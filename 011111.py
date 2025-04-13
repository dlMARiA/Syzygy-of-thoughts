import json

def process_jsonl(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            try:
                data = json.loads(line)
                answer = data.get('answer', '')
                # 提取答案中的最终结果
                parts = answer.split('####')
                if len(parts) > 1:
                    new_answer = parts[1].strip()
                else:
                    new_answer = answer
                data['answer'] = new_answer
                # 将处理后的 JSON 对象写回文件
                output_file.write(json.dumps(data) + '\n')
            except json.JSONDecodeError:
                print(f"Failed to parse JSON line: {line.strip()}")

if __name__ == "__main__":
    input_file_path = 'D:\pycharmcode\langchian_new\datasets\gsm8k\gsm8k_test.json'  # 替换为你的输入文件路径
    output_file_path = r'D:\pycharmcode\langchian_new\datasets\gsm8k\test.jsonl'  # 替换为你的输出文件路径
    process_jsonl(input_file_path, output_file_path)