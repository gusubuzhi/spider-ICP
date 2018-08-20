import random
import rk
import requests
from lxml import etree

def check_ip(name):
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.miitbeian.gov.cn/commons/left.jsp;jsessionid=W82S7WH28XCqxxT105quV3E6HrARNXaaI47UDne5gzUq1sq7Tjv3^!1316315234',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    s = requests.Session()
    response1 = s.get('http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action', headers=headers)
    response2 = s.get("http://www.miitbeian.gov.cn/getVerifyCode?"+str(random.randint(0,100)),headers = headers)

    # with open("capcha.gif",'wb') as f:
    #     f.write(response2.content)

    ruokuai = rk.RClient(user,password)
    yzm_request = ruokuai.rk_create(response2.content,3060)
    yzm =yzm_request['Result']
    data = {'validateValue': yzm}
    response3 = s.post("http://www.miitbeian.gov.cn/common/validate/validCode.action",data=data, headers = headers)

    data1 = [
      ('siteName', ''),
      ('condition', '1'),
      ('siteDomain', name),
      ('siteUrl', ''),
      ('mainLicense', ''),
      ('siteIp', ''),
      ('unitName', ''),
      ('mainUnitNature', '-1'),
      ('certType', '-1'),
      ('mainUnitCertNo', ''),
      ('verifyCode', yzm),
    ]

    response4 = s.post('http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_searchExecute.action', headers=headers, data=data1)
    html = response4.text
    data = etree.HTML(html)
    try:
        content = data.xpath('//td[@class="bxy"]/text()')
    except IndexError:
        print("输入的网址错误，请检查后再输入！！！")
        main()
    name = content[1]
    type = content[2]
    num = content[3]
    hostname = content[4]
    ip = content[5]
    time = content[6]
    print('--------------------------------')
    print('主办单位名称:',name)
    print('主办单位性质:',type)
    print('网站备案/许可证号:',num)
    print('网站名称:',hostname)
    print('网站首页网址:',ip)
    print('审核时间:',time)
    print('--------------------------------')

def main():
    name = input("输入要查询的网站域名(查询来源ICP备案网站---例：youku.com)：")
    check_ip(name)


if __name__ == "__main__":
    main()