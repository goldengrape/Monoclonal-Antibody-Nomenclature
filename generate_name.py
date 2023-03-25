import openai 
import time
import re 

sleep_time=60 
def query_gpt3(prompt,cooldown_time=3):
    global sleep_time
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{
                "role": "system", 
                "content": "You are a helpful philologist.",
                "role": "user", 
                "content": prompt}]
                )
            answer=response.choices[0].message.content.strip()
            time.sleep(cooldown_time)
            sleep_time = int(sleep_time/2)
            sleep_time = max(sleep_time, 10)
            break
        except:
            print(f"API error, retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
            sleep_time += 10
            if sleep_time > 120:
                print("API error, aborting...")
                answer=""
                break
    return answer

def generate_name(num,name_part,requirement):
    prompt=f'''Generate {num} of names for a monoclonal antibody. 
    The name MUST end with {name_part}.
    Following are the requirements:
    {requirement}
    The result should be in python list format.
    \["name1", "name2", "name3", ...\]
    Before you give me the answer, please be sure the name ends with {name_part}.
    '''
    answer=query_gpt3(prompt)
    # 提取结果
    try:
        answer=re.findall(r'\[".*"\]',answer)[0]
    except:
        answer="['']"
    # 将字符串转换为列表
    name_list=eval(answer)
    return name_list

def check_in_languages(lang_list,name, n=3,target_lang="English"):
    check_list={}
    for lang in lang_list:
        prompt=f'''
    Please find the word with the closest pronunciation or spelling to word part "{name.lower()}" in {lang}, 
    and translate the word into {target_lang}.
    It is possible that the word does not exist in {lang}.
    You still need to find out results.
    please return the top {n} results.
    The explaination should be as short as possible.
    Please return the results in python list format, 
    \["result1(translate1)","result2(translate2)"...]
    '''
        answer=query_gpt3(prompt)
        # 提取结果
        print(answer)
        # 从answer中提取json
        try:
            answer=re.findall(r'\[.*\]',answer)
        except:
            answer="{'':''}"
    # 将字符串转换为字典
    # try:
    #     check_list=eval(answer)
    # except:
    #     check_list={"":""}
        check_list[lang]=answer
    return check_list