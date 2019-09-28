# !/usr/bin/python2.7
# -*- coding:utf-8 -*-
# FileName: toutiao_favorites
# DateTime: 2019年02月03日13时03分12秒

import requests
import time
import math
import hashlib
import json
import xlwt

#https://www.toutiao.com/c/user/favourite/?page_type=2&user_id=4472044537&max_behot_time=0&count=20&as=A105DD98BF30D72&cp=5D8F608DD7A26E1&_signature=FreaYRARSz0e2KqGRLr9Bha3mn&max_repin_time=0

class ToutiaoFavorites(object):
    def __init__(self):
        self.User_Agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"
        self.cookie = 'CNZZDATA1259612802=1840461559-1546083028-%7C1563791143; csrftoken=600fc110c86a53ac068d0ea4851bed5a; _ga=GA1.2.2116125662.1546084107; sid_guard="d272fa05d0cbfe0d930a0268623043cd|1569654126|15552000|Thu\054 26-Mar-2020 07:02:06 GMT"; uuid="w:9c8b836bba1143d4a601243d9c08d7e4"; tt_webid=6716447668970948109; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16c196fa694c-0bb2ef8777587b-71236752-100200-16c196fa69531f; tt_webid=6716447668970948109; login_flag=2236fe2be14c39eefde4cbad09bbd030; sessionid=d272fa05d0cbfe0d930a0268623043cd; uid_tt=bfc8450a7fac5470453115ab17c3ee58; sid_tt=d272fa05d0cbfe0d930a0268623043cd; sso_uid_tt=f8af142d3e3cddc99014bdfb5b3ad337; toutiao_sso_user=ff48b52c8fea120980269e528bd82385; s_v_web_id=a5f4ef9af063c79b1a138d6ee4c1f839; __tasessionId=43cfag6pd1569656077010'
        self.max_repin_time = "0"
        self.signature = "FreaYRARSz0e2KqGRLr9Bha3mn"

    def get_as_cp(self):
        """获取构成地址的 as cp 参数"""
        int_t = int(math.floor(time.time()))    # 当前时间戳向下取整
        m = hashlib.md5()
        m.update(str(int_t).encode("utf-8"))
        md5_t = m.hexdigest().upper()   # 对取整后的当前时间戳进行md5加密，然后转大写

        hex_t = hex(int_t).upper()[2:]  # 对取整后的当前时间戳转16进制，转大写后去除前2个字符
        if len(hex_t) != 8:
            url_as = "A105DD98BF30D72"
            url_cp = "5D8F608DD7A26E1"
            return url_as, url_cp

        md5_t1 = md5_t[0:5]
        md5_t2 = md5_t[-5:]
        as_part = ""
        cp_part = ""
        for i in range(5):
            as_part += md5_t1[i] + hex_t[i]
            cp_part += hex_t[i+3] + md5_t2[i]
        url_as = "A1" + as_part + hex_t[-3:]
        url_cp = hex_t[0:3] + cp_part + "E1"
        return url_as, url_cp

    def format_time(self, timestamp):
        """转换收藏的时间戳格式为：xxxx年xx月xx日xx时xx分xx秒"""
        local_time = time.localtime(timestamp)
        pub_date = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        return pub_date

    def parse_info(self):
        """解析每一页里每一条收藏的信息，返回个收藏信息生成器"""
        url_as_cp = self.get_as_cp()
        for page_num in range(10):  # 总共有62页
            print("正在解析第 %d 页......" % (page_num+1))
            url_as = url_as_cp[0]
            url_cp = url_as_cp[1]
            url = "https://www.toutiao.com/c/user/favourite/?page_type=2&user_id=4472044537" \
                  "&max_behot_time=0&count=20&as=" + url_as + "&cp=" + url_cp \
                  + "&_signature=" + self.signature + "&max_repin_time=" + self.max_repin_time  # xxxxxx为头条账户ID
            headers = {
                "Host": "www.toutiao.com",
                "accept": "application/json, text/javascript",
                "accept-language": "zh-CN",
                "cookie": self.cookie,
                "referer": "https://www.toutiao.com/c/user/4472044537/",
                "user-agent": self.User_Agent
            }
            time.sleep(1)
            response = requests.get(url, headers=headers)
            page_data = response.json()  # page_data为字典类型数据
            favorites = page_data["data"]

            self.max_repin_time = str(page_data["max_repin_time"])  # 获取此次请求返回的max_repin_time， 用于构成下次请求的url
            if len(favorites) <= 0:
                break
            for i in range(len(favorites)):
                timestamp = favorites[i].get("behot_time", 0)
                info = {
                    "No.": page_num * 20 + i + 1,
                    u"文章分类": favorites[i].get("chinese_tag", u"未知分类"),
                    u"文章标题": favorites[i].get("title", u"未知标题"),
                    u"文章链接": "http://www.toutiao.com"+favorites[i].get("source_url", u"未知链接"),
                    u"发布时间": self.format_time(timestamp)
                }
                yield info

    def save_info(self, save_choice):
        """保存收藏信息"""
        def write_to_execl(info):
            """将1条收藏信息写入execl表格"""
            ws.write(each["No."], 0, each[u"文章分类"])
            ws.write(each["No."], 1, each[u"文章标题"])
            ws.write(each["No."], 2, each[u"文章链接"])
            ws.write(each["No."], 3, each[u"发布时间"])

        def write_to_json(info):
            """将1条收藏信息写入json文件"""
            article_info_json = json.dumps(each, ensure_ascii=False)
            f.write(article_info_json.encode("utf-8") + ",\n")

        if save_choice in ["1", "3"]:  # 创建1个表格用于保存所有收藏信息
            wb = xlwt.Workbook()
            ws = wb.add_sheet("favorites_infos", cell_overwrite_ok=True)
            row0 = [u"文章分类", u"文章标题", u"文章链接", u"发布时间"]
            style0 = xlwt.easyxf("font:name Times New Roman, color-index red, bold on", num_format_str="#,##0.00")
            for i in range(4):
                ws.write(0, i, row0[i], style0)
        if save_choice in ["2", "3"]:  # 创建1个json文件用于保存所有收藏信息
            f = open("./toutiao_favorites.json", "w")
            f.write("[")

        if save_choice == "1":
            for each in self.parse_info():  # 迭代收藏信息生成器，全部写入execl表格
                write_to_execl(each)
        if save_choice == "2":
            for each in self.parse_info():  # 迭代收藏信息生成器，全部写入json文件
                write_to_json(each)
        if save_choice == "3":
            for each in self.parse_info():  # 迭代收藏信息生成器，全部分别写入execl表格、json文件
                write_to_execl(each)
                write_to_json(each)

        if save_choice in ["1", "3"]:
            wb.save("./toutiao_favorites.xls")   # 保存execl表格
            print("已成功保存为execl")
        if save_choice in ["2", "3"]:
            f.write("]")
            f.close()    # 关闭保存json文件
            print("已成功保存为json")


def main():
    print("=" * 10+"MENU"+"="*10)
    print("1：保存为execl\n2：保存为json\n3：保存为execl、json各1份\n0：退出")
    print("=" * 24)

    toutiao = ToutiaoFavorites()
    save_choice = "1"
    while True:
        if save_choice in ["1", "2", "3"]:
            toutiao.save_info(save_choice)
            break
        elif save_choice == "0":
            break
        else:
            save_choice = raw_input("序号错误，请重新输入：")
    print("谢谢使用")

if __name__ == "__main__":
    main()










