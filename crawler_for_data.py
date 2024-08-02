import requests
import gzip
import json
from io import BytesIO
import time

# url1 是商品信息页
# url2 是商品趋势页
# url3 是中文翻译页，目前还没有实现。原因是这个POST请求的fm_token是动态的，目前还没有找到生成规则。不过python提供有翻译库，可以直接调用。所以这个需求暂时还没有做，后续可以考虑加上。

def get_and_print_response(url, headers):
    try:
        # 发起 GET 请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 打印响应头以确认 Content-Encoding
        # print("Response Headers:", response.headers)

        # 检查内容编码是否为 gzip，并且确认内容的前两个字节是否为 JSON 的标志
        content_start = response.content[:2]
        if response.headers.get('Content-Encoding') == 'gzip' and content_start != b'{"':
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                body = gz.read()
        else:
            body = response.content

        # 打印响应体内容
        # print("Response Body:", body.decode('utf-8'))

        return body

    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None
    

# def post_and_print_response(url, headers):
#     try:
#         # 发起 POST 请求
#         response = requests.post(url, headers=headers)
#         response.raise_for_status()  # 检查请求是否成功

#         # 打印响应头以确认 Content-Encoding
#         # print("Response Headers:", response.headers)

#         # 检查内容编码是否为 gzip，并且确认内容的前两个字节是否为 JSON 的标志
#         content_start = response.content[:2]
#         if response.headers.get('Content-Encoding') == 'gzip' and content_start != b'{"':
#             with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
#                 body = gz.read()
#         else:
#             body = response.content

#         # 打印响应体内容
#         # print("Response Body:", body.decode('utf-8'))

#         return body
#     except requests.RequestException as e:
#         print(f"Error making request: {e}")
#         return None


def process_response(body):
    try:
        # 反序列化 JSON 数据
        response_data = json.loads(body)

        # 使用 json.dumps 格式化输出
        formatted_response = json.dumps(response_data, indent=2, ensure_ascii=False)
        print("Formatted Response JSON:", formatted_response)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

def main():
    # Info
    url1 = "https://www.fastmoss.com/api/goods/base?product_id=1729643078414797473&tab=1&_time=1722601030&cnonce=61119741"
    # Trend
    url2 = "https://www.fastmoss.com/api/goods/analyse?product_id=1729643078414797473&d_type=3&_time=1722601030&cnonce=81459272"

    # # Chinese translation
    # url3 = "https://www.fastmoss.com/api/translate?_time=1722602130&cnonce=52159821" 


    # Headers for info
    headers1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        # "Accept": "*/*",
        # "Accept-Encoding": "gzip, deflate, br, zstd",
        # "Accept-Language": "en-US,en;q=0.9",
        # "Referer": "https://www.fastmoss.com/zh/e-commerce/detail/1729418496836080191",
        # "Sec-CH-UA": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        # "Sec-CH-UA-Mobile": "?0",
        # "Sec-CH-UA-Platform": '"Windows"',
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "same-origin",
        "Fm-Sign": "d9acf0771d83cc4bd7de4182df6f0e67",
        # "Lang": "ZH_CN",
        # "Priority": "u=1, i",
        # "Timezone": "Asia/Shanghai",
        "Cookie": "fd_id=hnQPMXr3sWc7BJ8omIbgLYf091NpDC24; vis_fid=66ac8eaeb92615055271722584750.7587; fp_visid=08db8fb266229124abc3c7a27f34dee4; _gcl_au=1.1.1809724902.1722584758; _ga=GA1.1.4480884.1722584758; _fbp=fb.1.1722584761304.505169350391205820; fd_tk_exp=1723880881; fd_tk=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM4ODA4ODEsInN1YiI6IjhiNTRjZjM5YjEzNjBkYTE4NDRhNGJhMTYxN2M0MWYzIiwibmJmIjoxNzIyNTg0ODgxLCJhdWQiOnsidWlkIjo0NTY2NzczLCJ1bmlvbmlkIjoib3RXMXY1MDBCSjUtRWxHTllkSWVoWGt1LWNIcyIsIm1jX29wZW5pZCI6IiIsIm5pY2tuYW1lIjoiRmFzdE1vc3PnlKjmiLciLCJjcmVhdGVkX2F0IjoxNzIwMjQ2MTkzLCJjcmVhdGVkX2RhdGUiOiIyMDI0LTA3LTA2IiwibG9naW5fc291cmNlIjoicGMiLCJ2aXNpdG9yX2lkIjoiMDhkYjhmYjI2NjIyOTEyNGFiYzNjN2EyN2YzNGRlZTQiLCJkb21haW4iOiJ3d3cuZmFzdG1vc3MuY29tIiwiZnBfdmlzaWQiOiIxZDE5OWNmMzVjZGQxZGZlODRlZmQxMTAyODgwZDQyMSJ9LCJpYXQiOjE3MjI1ODQ4ODEsImp0aSI6IjhiNTRjZjM5YjEzNjBkYTE4NDRhNGJhMTYxN2M0MWYzIiwiaXNzIjoid3d3LmZhc3Rtb3NzLmNvbSIsInN0YXR1cyI6MSwiZGF0YSI6bnVsbH0.Alc_JpKKLdutuxYcy2SwO_xnpaDuwRlkRfpc_YUjJf4; _ga_GD8ST04HB5=GS1.1.1722589649.2.0.1722589649.60.0.0; Hm_lvt_6ada669245fc6950ae4a2c0a86931766=1722589651; HMACCOUNT=9E01919F74B26C28; _uetsid=417bfd1050a311efb340e5f483f7dd11|11wdtb3|2|fnz|0|1675; _uetvid=417c228050a311efac2d7fd52be80301|1vwfvlv|1722601021240|4|1|bat.bing.com/p/insights/c/z; Hm_lpvt_6ada669245fc6950ae4a2c0a86931766=1722601030"
    }

    # Headers for trend
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Fm-Sign": "7b504e47582861329479f86fbd436043",
        "Cookie": "fd_id=hnQPMXr3sWc7BJ8omIbgLYf091NpDC24; vis_fid=66ac8eaeb92615055271722584750.7587; fp_visid=08db8fb266229124abc3c7a27f34dee4; _gcl_au=1.1.1809724902.1722584758; _ga=GA1.1.4480884.1722584758; _fbp=fb.1.1722584761304.505169350391205820; fd_tk_exp=1723880881; fd_tk=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM4ODA4ODEsInN1YiI6IjhiNTRjZjM5YjEzNjBkYTE4NDRhNGJhMTYxN2M0MWYzIiwibmJmIjoxNzIyNTg0ODgxLCJhdWQiOnsidWlkIjo0NTY2NzczLCJ1bmlvbmlkIjoib3RXMXY1MDBCSjUtRWxHTllkSWVoWGt1LWNIcyIsIm1jX29wZW5pZCI6IiIsIm5pY2tuYW1lIjoiRmFzdE1vc3PnlKjmiLciLCJjcmVhdGVkX2F0IjoxNzIwMjQ2MTkzLCJjcmVhdGVkX2RhdGUiOiIyMDI0LTA3LTA2IiwibG9naW5fc291cmNlIjoicGMiLCJ2aXNpdG9yX2lkIjoiMDhkYjhmYjI2NjIyOTEyNGFiYzNjN2EyN2YzNGRlZTQiLCJkb21haW4iOiJ3d3cuZmFzdG1vc3MuY29tIiwiZnBfdmlzaWQiOiIxZDE5OWNmMzVjZGQxZGZlODRlZmQxMTAyODgwZDQyMSJ9LCJpYXQiOjE3MjI1ODQ4ODEsImp0aSI6IjhiNTRjZjM5YjEzNjBkYTE4NDRhNGJhMTYxN2M0MWYzIiwiaXNzIjoid3d3LmZhc3Rtb3NzLmNvbSIsInN0YXR1cyI6MSwiZGF0YSI6bnVsbH0.Alc_JpKKLdutuxYcy2SwO_xnpaDuwRlkRfpc_YUjJf4; _ga_GD8ST04HB5=GS1.1.1722589649.2.0.1722589649.60.0.0; Hm_lvt_6ada669245fc6950ae4a2c0a86931766=1722589651; HMACCOUNT=9E01919F74B26C28; _uetsid=417bfd1050a311efb340e5f483f7dd11|11wdtb3|2|fnz|0|1675; _uetvid=417c228050a311efac2d7fd52be80301|1vwfvlv|1722601021240|4|1|bat.bing.com/p/insights/c/z; Hm_lpvt_6ada669245fc6950ae4a2c0a86931766=1722601030"
    }

    # # headers for Chinese translation
    # headers3 = {
    #     "content-type": "application/json;charset=utf-8",
    #     "accept": "application/json",
    #     "Referer": "https://www.fastmoss.com/zh/e-commerce/detail/1729643078414797473",

    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    #     "Fm-Sign": "252b4f2b27379ef4d7823621d690bd6d",
    #     "Cookie": "fd_id=hnQPMXr3sWc7BJ8omIbgLYf091NpDC24; vis_fid=66ac8eaeb92615055271722584750.7587; fp_visid=08db8fb266229124abc3c7a27f34dee4; _gcl_au=1.1.1809724902.1722584758; _ga=GA1.1.4480884.1722584758; _fbp=fb.1.1722584761304.505169350391205820; fd_tk_exp=1723880881; fd_tk=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM4ODA4ODEsInN1YiI6IjhiNTRjZjM5YjEzNjBkYTE4NDRhNGJhMTYxN2M0MWYzIiwibmJmIjoxNzIyNTg0ODgxLCJhdWQiOnsidWlkIjo0NTY2NzczLCJ1bmlvbmlkIjoib3RXMXY1MDBCSjUtRWxHTllkSWVoWGt1LWNIcyIsIm1jX29wZW5pZCI6IiIsIm5pY2tuYW1lIjoiRmFzdE1vc3PnlKjmiLciLCJjcmVhdGVkX2F0IjoxNzIwMjQ2MTkzLCJjcmVhdGVkX2RhdGUiOiIyMDI0LTA3LTA2IiwibG9naW5fc291cmNlIjoicGMiLCJ2aXNpdG9yX2lkIjoiMDhkYjhmYjI2NjIyOTEyNGFiYzNjN2EyN2YzNGRlZTQiLCJkb21haW4iOiJ3d3cuZmFzdG1vc3MuY29tIiwiZnBfdmlzaWQiOiIxZDE5OWNmMzVjZGQxZGZlODRlZmQxMTAyODgwZDQyMSJ9LCJpYXQiOjE3MjI1ODQ4ODEsImp0aSI6IjhiNTRjZjM5YjEzNjBkYTE4NDRhNGJhMTYxN2M0MWYzIiwiaXNzIjoid3d3LmZhc3Rtb3NzLmNvbSIsInN0YXR1cyI6MSwiZGF0YSI6bnVsbH0.Alc_JpKKLdutuxYcy2SwO_xnpaDuwRlkRfpc_YUjJf4; _ga_GD8ST04HB5=GS1.1.1722589649.2.0.1722589649.60.0.0; Hm_lvt_6ada669245fc6950ae4a2c0a86931766=1722589651; HMACCOUNT=9E01919F74B26C28; _uetsid=417bfd1050a311efb340e5f483f7dd11|11wdtb3|2|fnz|0|1675; Hm_lpvt_6ada669245fc6950ae4a2c0a86931766=1722602127; _uetvid=417c228050a311efac2d7fd52be80301|1vwfvlv|1722602127266|6|1|bat.bing.com/p/insights/c/z"
    # }


    body1 = get_and_print_response(url1, headers1)
    if body1:
        process_response(body1)

    time.sleep(3)

    body2 = get_and_print_response(url2, headers2)
    if body2:
        process_response(body2)

    # body3 = post_and_print_response(url3, headers3)
    # if body3:
    #     process_response(body3)

    

if __name__ == "__main__":
    main()
