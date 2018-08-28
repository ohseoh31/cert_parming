from selenium import webdriver
import re
import pymysql
from datetime import datetime

def unZip():
    print('unzip')
#
# /html/body/table/tbody/tr[4]/td[2]/a
# /html/body/table/tbody/tr[5]/td[2]/a
# /html/body/table/tbody/tr[6]/td[2]/a

def selinumDownload():
    driver = webdriver.Chrome()
    driver.get("http://107.174.85.141/cert/")

    i = 4
    while True:
        try:
            download_url = '/html/body/table/tbody/tr[' + str(
                i) + ']/td[2]/a'
            driver.find_element_by_xpath(download_url).click()
            i = i+1
        except :
            print("end")


'''
서버 (http://107.174.85.141/cert)
1. 피해자의 일련번호 - 피해시각(서버에 피해자의 공인인증서가 업로드된 시간)
- 국가코드

- 피해자의 이름
- 은행명
- 계좌번호
- IP주소
'''


'''
val_at = re.findall(find_value_at, text)

            if val != [] and val_at == []:
                count +=1
                self.val_List.append([count, val[0][0].upper(), val[0][1].upper()])
'''


#공인인증서 정보 추출
def find_people_info(fileName):
    #fileName = 'signCert.cert'
    cert = open(fileName , 'r')
    text = cert.readline()
    #print (text)
    reg_info = '^cn=([가-힣]+)\(\)([0-z]+),ou=([a-zA-Z]+),ou=([a-zA-Z]+),o=([a-zA-Z]+),c=([a-zA-Z]+)'

    cert_value = re.findall(reg_info, text)
    # print (cert_value[0][0])
    # print(cert_value[0][1])
    # print(cert_value[0][2])
    # print(cert_value[0][3])
    # print(cert_value[0][4])
    # print(cert_value[0][5])

    #Name 계좌번호
    cert_list =[]

    for i in range(0, len(cert_value[0])):
        cert_list.append(cert_value[0][i])

    print (cert_list)
    return cert_list
    #sql_list.append()

def inputDB(sql_list) : #insert log file into mysql database
    conn = pymysql.connect(host='localhost', user='root', password='1234',
                           db='cert_info', charset='utf8')

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    curs = conn.cursor()
    #insert into cert(date, bank_info, account_number, country, IP) values ('2018-08-28', '', 1, '', '' );
    sql = """insert into cert(date, bank_info, account_number, country, IP) values ( %s, %s, %s, %s, %s )"""

    for i in range(0, len(sql_list)):
        print ("www")
        #date, bank_info, accountnumber, ip, country
        curs.execute(sql, (formatted_date, sql_list[i][0], float(sql_list[i][1]), sql_list[i][2], sql_list[i][5],'IP'))
        #curs.execute(sql, ('2018-08-26', 'name', 1, 'kr', 'ip'))
    conn.commit()

if __name__ == "__main__":
    #selinumDownload()

    fileName = 'signCert.cert'
    sql_list = []

    cert_list = find_people_info(fileName)

    sql_list.append(cert_list)
    inputDB(sql_list)