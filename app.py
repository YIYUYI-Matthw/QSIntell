# coding:utf-8
import time

from flask import Flask, render_template, redirect, request, jsonify
import re
import requests

app = Flask(__name__)

ans1 = "身份证丢了，需要补办。首先，需要前往当地公安机关身份证窗口或通过在线预约方式申请挂失并预约时间。接着，到公安机关办理补领身份证的手续，需要提交申请表、身份证明等材料，并缴纳一定的费用。在办理过程中，公安机关会核对身份并采集指纹等个人信息。办理完成后，将获得新的身份证和挂失证明，并在规定的时间内领取。" + \
       "出处 [1] 市公安局.jsonl：" + \
       "知识名称: 居民身份证换领>居民身份证挂失信息核查服务-依据 关键字: 居民身份证挂失信息核查服务 知识内容: 《中华人民共和国居民身份证法》第二条：居住在中华人民共和国境内的年满十六周岁的中国公民，应当依照本法的规定申请领取居民身份证；未满十六周岁的中国公民，可以依照本法的规定申请领取居民身份证。\n第七条：公民应当自年满十六周岁之日起三个月内，向常住户口所在地的公安机关申请领取居民身份证。未满十六周岁的公民，由监护人代为申请领取居民身份证。\n第十一条：国家决定换发新一代居民身份证、居民身份证有效期满、公民姓名变更或者证件严重损坏不能辨认的，公民应当换领新证；居民身份证登记项目出现错误的，公安机关应当及时更正，换发新证；领取新证时，必须交回原证。居民身份证丢失的，应当申请补领。未满十六周岁公民的居民身份证有前款情形的，可以申请换领、换发或者补领新证。公民办理常住户口迁移手续时，公安机关应当在居民身份证的机读项目中记载公民常住户口所在地住址变动的情况，并告知本人。\n第十二条：公民申请领取、换领、补领居民身份证，公安机关应当按照规定及时予以办理。公安机关应当自公民提交《居民身份证申领登记表》之日起六十日内发放居民身份证；交通不便的地区，办理时间可以适当延长，但延长的时间不得超过三十日。公民在申请领取、换领、补领居民身份证期间，急需使用居民身份证的，可以申请领取临时居民身份证，公安机关应当按照规定及时予以办理。具体办法由国务院公安部门规定。\n《中华人民共和国临时居民身份证管理办法》第二条：居住在中华人民共和国境内的中国公民，在申请领取换领、补领居民身份证期间，急需使用居民身份证的，可以申请领取临时居民身份证。\n《关于建立居民身份证异地受理挂失申报和丢失招领制度的意见》（公通字〔2015〕34号） 地域: 海南省三亚市 实施单位: 市公安局 " + \
       "出处 [2] 市公安局.jsonl：" + \
       "知识名称: 居民身份证挂失申报-依据 关键字: 居民身份证挂失申报 知识内容: 《中华人民共和国居民身份证法》第二条：居住在中华人民共和国境内的年满十六周岁的中国公民，应当依照本法的规定申请领取居民身份证；未满十六周岁的中国公民，可以依照本法的规定申请领取居民身份证。\n第七条：公民应当自年满十六周岁之日起三个月内，向常住户口所在地的公安机关申请领取居民身份证。未满十六周岁的公民，由监护人代为申请领取居民身份证。\n第十一条：国家决定换发新一代居民身份证、居民身份证有效期满、公民姓名变更或者证件严重损坏不能辨认的，公民应当换领新证；居民身份证登记项目出现错误的，公安机关应当及时更正，换发新证；领取新证时，必须交回原证。居民身份证丢失的，应当申请补领。未满十六周岁公民的居民身份证有前款情形的，可以申请换领、换发或者补领新证。公民办理常住户口迁移手续时，公安机关应当在居民身份证的机读项目中记载公民常住户口所在地住址变动的情况，并告知本人。\n第十二条：公民申请领取、换领、补领居民身份证，公安机关应当按照规定及时予以办理。公安机关应当自公民提交《居民身份证申领登记表》之日起六十日内发放居民身份证；交通不便的地区，办理时间可以适当延长，但延长的时间不得超过三十日。公民在申请领取、换领、补领居民身份证期间，急需使用居民身份证的，可以申请领取临时居民身份证，公安机关应当按照规定及时予以办理。具体办法由国务院公安部门规定。\n《中华人民共和国临时居民身份证管理办法》第二条：居住在中华人民共和国境内的中国公民，在申请领取换领、补领居民身份证期间，急需使用居民身份证的，可以申请领取临时居民身份证。\n《关于建立居民身份证异地受理挂失申报和丢失招领制度的意见》（公通字〔2015〕34号） 地域: 海南省三亚市 实施单位: 市公安局 " + \
       "出处 [3] 市公安局.jsonl：" + \
       "知识名称: 居民身份证补领>丢失异地补领居民身份证-依据 关键字: 居民身份证 知识内容: 《中华人民共和国居民身份证法》第二条：居住在中华人民共和国境内的年满十六周岁的中国公民，应当依照本法的规定申请领取居民身份证；未满十六周岁的中国公民，可以依照本法的规定申请领取居民身份证。\n第七条：公民应当自年满十六周岁之日起三个月内，向常住户口所在地的公安机关申请领取居民身份证。未满十六周岁的公民，由监护人代为申请领取居民身份证。\n第十一条：国家决定换发新一代居民身份证、居民身份证有效期满、公民姓名变更或者证件严重"

ans2 = "根据已知信息，机动车维修经营备案的承诺办结时限为5个工作日，法定办结时限为5个工作日。" + \
       "出处 [1] 海南省三亚市天涯区交通运输和安全生产监管局.jsonl：" + \
       "知识名称: 机动车维修经营>机动车维修经营备案-受理条件 关键字: 机动车维修 知识内容: 已经取得营业执照的企业法人。 地域: 海南省三亚市天涯区 实施单位: 海南省三亚市天涯区交通运输和安全生产监管局 " + \
       "出处 [2] 海南省三亚市天涯区交通运输和安全生产监管局.jsonl：" + \
       "知识名称: 机动车维修经营>机动车维修经营备案-办理结果 关键字: 机动车维修 知识内容: 结果名称：机动车维修经营备案表;\n结果样本：机动车维修经营备案表（样表）.pdf 地域: 海南省三亚市天涯区 实施单位: 海南省三亚市天涯区交通运输和安全生产监管局  知识名称: 机动车维修经营>机动车维修经营备案-收费 关键字: 机动车维修 知识内容: 无收费项 地域: 海南省三亚市天涯区 实施单位: 海南省三亚市天涯区交通运输和安全生产监管局 " + \
       "出处 [3] 海南省三亚市天涯区交通运输和安全生产监管局.jsonl：" + \
       "知识名称: 机动车维修经营>机动车维修连锁经营备案-受理条件 关键字: 机动车,机动车维修经营备案 知识内容: 总部已经完成备案的维修企业。 地域: 海南省三亚市天涯区 实施单位: 海南省三亚市天涯区交通运输和安全生产监管局" + \
       "出处 [4] 海南省三亚市天涯区交通运输和安全生产监管局.jsonl：" + \
       "知识名称: 机动车维修经营>机动车维修连锁经营备案-办理结果 关键字: 机动车,机动车维修经营备案 知识内容: 结果名称：机动车维修经营备案公告;\n结果样本：机动车维修经营备案表（样表）.pdf 地域: 海南省三亚市天涯区 实施单位: 海南省三亚市天涯区交通运输和安全生产监管局  知识名称: 机动车维修经营>机动车维修连锁经营备案-收费 关键字: 机动车,机动车维修经营备案 知识内容: 无收费项 地域: 海南省三亚市天涯区 实施单位: 海南省三亚市天涯区交通运输和安全生产监管局 " + \
       "出处 [5] 海南省三亚市天涯区交通运输和安全生产监管局.jsonl：" + \
       "知识名称: 机动车维修经营>机动车维修连锁经营备案-时限 关键字: 机动车,机动车维修经营备案 知识内容: 承诺办结时限：5个工作日\n法定办结时限：5个工作日 地域: 海南省三亚市天涯区 实施单位: 海南省三亚市天涯区交通运输和安全生产监管局  知识名称: 机动车维修经营>机动车维修连锁经营备案-投诉方式 关键字: 机动车,机动车维修经营备案 知识内容: 0898-12345 地域: 海南省三亚市天涯区 实施单位: 海南省三亚市天涯区交通运输和安全生产监管局 "


def extract(main_str="", source_list=None):
    keywords = set()
    res_list = []
    for source in source_list[:5]:
        keyword, ans_item = re_extract(source)
        if keyword == "-":
            continue
        keywords.add(keyword)
        res_list.append(ans_item)
    main_str_lines = main_str.split("\\n")
    if len(main_str_lines) == 1:
        return {'main_str': main_str, 'keywords': list(keywords), 'res_list': res_list}
    main_res = ''
    for line in main_str_lines:
        main_res += '<div>' + line + '</div>'
    return {'main_str': main_res, 'keywords': list(keywords), 'res_list': res_list}


def re_extract(source_str):
    re_keyword = "关键字: (.*?) 知识内容:"
    re_keyword_pattern = re.compile(re_keyword, flags=re.M | re.S)
    cands = re_keyword_pattern.findall(source_str)
    if len(cands) > 0:
        keyword = re_keyword_pattern.findall(source_str)[0]

        re_head = "知识名称: (.*?) 关键字:"
        re_head_pattern = re.compile(re_head, flags=re.M | re.S)
        head = re_head_pattern.findall(source_str)[0]

        re_content = "知识内容: (.*)"
        re_content_pattern = re.compile(re_content, flags=re.M | re.S)
        content_process = ''
        tmp = re_content_pattern.findall(source_str)[0].replace("\\n", "\n")
        for line in tmp.split("\n"):
            content_process += '<div style = "margin-top: 5px">' + line + '</div>'
        return keyword, {'head': head, 'content': content_process}
    return '-', '-'


@app.route('/')
def hello_world():  # put application's code here
    return redirect("/qsIntell")


@app.route("/qsIntell")
def qs():
    return render_template("QSGPT.html")


@app.route("/queryLLM")
def queryLLM():
    query = request.args.get("query")
    url = "http://10.126.62.38:8866/queryLLM?query=" + query
    ans_raw = requests.get(url)
    print(ans_raw)
    ans_raw.encoding = 'utf-8'
    ans_raw = eval(ans_raw.text)
    return jsonify(extract(ans_raw["回答"], ans_raw["出处文档"]))


def queryHttp(query, model="ChatGLM"):
    url = "http://10.126.62.38:8000/queryLLM?query=" + query
    ans_raw = requests.get(url)
    ans_raw.encoding = 'utf-8'
    ans_raw = eval(ans_raw.text)
    ans = ans_raw["回答"] + str(ans_raw["出处文档"])
    return jsonify(extract(ans[2:-2]))


@app.route("/queryLLM_raw")
def queryLLM_local():
    query = request.args.get("query")
    model = request.args.get("model")
    if "身份证丢了怎么补办" in query:
        time.sleep(2)
        main_str = ans1.split("出处")[0]
        key_list = ans1.split("出处")[1:]
        return jsonify(extract(main_str=main_str, source_list=key_list))
    elif "机动车维修经营备案" in query:
        time.sleep(1.5)
        return jsonify(extract(ans2))
    else:
        return queryHttp(query, model)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    # extract(ans)
