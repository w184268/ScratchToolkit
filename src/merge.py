import argparse
import zipfile
import json
import os
import base64
from pathlib import Path
import uuid

class ScratchProject:
    def __init__(self, id):
        self.id = id

    def get_nested_depth3(self, blocks, current_depth=0):
        block_id = self.id
        if block_id not in blocks:
            return current_depth
        block = blocks[block_id]
        next_depth = current_depth + 1
        next_block_id = block.get('next', '')
        inputs_depth = next_depth
        
        if 'inputs' in block:
            for input_name, input_value in block['inputs'].items():
                if isinstance(input_value[1], list) and len(input_value[1]) == 2:
                    if isinstance(input_value[1][1], str):
                        if input_value[1][1] in blocks:
                            inputs_depth = max(inputs_depth, ScratchProject(input_value[1][1]).get_nested_depth3(blocks, next_depth))
                    elif isinstance(input_value[1][1], int):
                        if str(input_value[1][1]) in blocks:
                            inputs_depth = max(inputs_depth, ScratchProject(str(input_value[1][1])).get_nested_depth3(blocks, next_depth))
        
        if isinstance(next_block_id, str) and next_block_id:
            if next_block_id in blocks:
                next_depth = max(next_depth, ScratchProject(next_block_id).get_nested_depth3(blocks, next_depth))
        elif isinstance(next_block_id, int):
            if str(next_block_id) in blocks:
                next_depth = max(next_depth, ScratchProject(str(next_block_id)).get_nested_depth3(blocks, next_depth))
        
        return max(next_depth, inputs_depth)

def load_scratch_project(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        with zip_ref.open('project.json') as project_file:
            project_data = json.load(project_file)
    
    # 初始化assets字段，如果不存在则创建一个空列表
    if 'assets' not in project_data:
        project_data['assets'] = []
    
    # 提取资源文件
    assets = project_data['assets']
    for asset in assets:
        asset_name = asset['assetId'] + '.' + asset['dataFormat']
        if asset_name in zip_ref.namelist():
            with zip_ref.open(asset_name) as asset_file:
                asset['data'] = base64.b64encode(asset_file.read()).decode('utf-8')
    
    return project_data

def save_scratch_project(project_data, file_path):
    # 创建临时目录来存储合并后的项目文件
    temp_dir = Path('temp_merged_project')
    if temp_dir.exists():
        for item in temp_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                os.rmdir(item)
        os.rmdir(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存合并后的project.json
    with open(temp_dir / 'project.json', 'w') as project_file:
        json.dump(project_data, project_file)
    
    # 将资源文件复制到临时目录
    for asset in project_data['assets']:
        asset_name = asset['assetId'] + '.' + asset['dataFormat']
        asset_data = asset['data']
        
        # 解码Base64字符串并保存资源文件
        decoded_data = base64.b64decode(asset_data)
        asset_file_path = temp_dir / asset_name
        with open(asset_file_path, 'wb') as asset_file:
            asset_file.write(decoded_data)
        print(f"提取并保存了资源文件: {asset_file_path}")
    
    # 保存合并后的.sb3文件
    with zipfile.ZipFile(file_path, 'w') as zip_ref:
        for file in temp_dir.iterdir():
            zip_ref.write(file, file.name)
    
    # 删除临时目录
    for item in temp_dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            os.rmdir(item)
    os.rmdir(temp_dir)

def generate_unique_id():
    return str(uuid.uuid4())

def remap_block_ids(block, blocks, block_id_map):
    for key, value in block.items():
        if key == 'parent' or key == 'next':
            if value in block_id_map:
                block[key] = block_id_map[value]
        elif key == 'inputs':
            for input_name, input_value in block['inputs'].items():
                if isinstance(input_value[1], list) and len(input_value[1]) == 2:
                    if isinstance(input_value[1][1], str):
                        if input_value[1][1] in block_id_map:
                            input_value[1][1] = block_id_map[input_value[1][1]]
                    elif isinstance(input_value[1][1], int):
                        input_value[1][1] = str(input_value[1][1])
                        if input_value[1][1] in block_id_map:
                            input_value[1][1] = block_id_map[input_value[1][1]]
    return block

def merge_projects(project1, project2):
    # 合并角色
    merged_targets = project1['targets'] + project2['targets']
    
    # 合并资源文件（costumes, sounds）
    merged_assets = project1.get('assets', []) + project2.get('assets', [])
    
    # 合并元数据
    merged_metadata = {**project1['meta'], **project2['meta']}
    
    # 合并变量
    merged_variables = project1.get('variables', []) + project2.get('variables', [])
    
    # 合并自定义积木
    merged_custom_blocks = {**project1.get('customBlocks', {}), **project2.get('customBlocks', {})}
    
    # 处理积木块ID的唯一性
    block_id_map1 = {}
    block_id_map2 = {}
    
    for target in project1['targets']:
        new_blocks = {}
        for block_id, block in target['blocks'].items():
            new_id = generate_unique_id()
            block_id_map1[block_id] = new_id
            new_blocks[new_id] = block
        target['blocks'] = new_blocks
    
    for target in project2['targets']:
        new_blocks = {}
        for block_id, block in target['blocks'].items():
            new_id = generate_unique_id()
            block_id_map2[block_id] = new_id
            new_blocks[new_id] = block
        target['blocks'] = new_blocks
    
    # 重新映射积木块中的ID
    for target in project1['targets']:
        for block_id, block in target['blocks'].items():
            print(block)
            if isinstance(block, dict):remap_block_ids(block, target['blocks'], block_id_map1)
    
    for target in project2['targets']:
        for block_id, block in target['blocks'].items():
            if isinstance(block, dict):remap_block_ids(block, target['blocks'], block_id_map2)
    
    # 合并项目
    merged_project = {
        'targets': merged_targets,
        'assets': merged_assets,
        'metadata': merged_metadata,
        'variables': merged_variables,
        'customBlocks': merged_custom_blocks
    }
    
    return merged_project

def extract_svg_images(project, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for target_index, target in enumerate(project['targets']):
        target_name = target['name'].replace(' ', '_').lower()  # 将角色名称转换为文件夹名
        costumes_directory = os.path.join(output_directory, target_name)
        if not os.path.exists(costumes_directory):
            os.makedirs(costumes_directory)
        
        for costume_index, costume in enumerate(target['costumes']):
            if costume['assetId'] == 'ImageVectorType':  # 检查是否为SVG类型
                svg_data = costume['data']
                # 解码Base64字符串
                decoded_svg = base64.b64decode(svg_data)
                # 保存SVG文件
                costume_name = costume['name'].replace(' ', '_').lower()  # 将外观名称转换为文件名
                svg_file_path = os.path.join(costumes_directory, f"{costume_name}_{costume_index}.svg")
                with open(svg_file_path, 'wb') as svg_file:
                    svg_file.write(decoded_svg)
                print(f"提取并保存了SVG图片: {svg_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Merge two Scratch 3.0 project files (.sb3).")
    parser.add_argument('file_path1', type=str, help="Path to the first .sb3 file.")
    parser.add_argument('file_path2', type=str, help="Path to the second .sb3 file.")
    parser.add_argument('-o', '--output', type=str, default='merged_project.sb3', help="Path to the output merged .sb3 file.")
    
    args = parser.parse_args()
    
    # 使用Path.resolve确保路径绝对化并解析符号链接
    file_path1 = Path(args.file_path1).resolve()
    file_path2 = Path(args.file_path2).resolve()
    output_path = Path(args.output).resolve()
    
    if not file_path1.exists():
        print(f"文件 {file_path1} 不存在")
        return
    
    if not file_path2.exists():
        print(f"文件 {file_path2} 不存在")
        return
    
    # 加载两个Scratch项目文件
    project1 = load_scratch_project(file_path1)
    project2 = load_scratch_project(file_path2)
    
    # 合并项目
    merged_project = merge_projects(project1, project2)
    
    # 提取并保存SVG图片
    extract_svg_images(merged_project, 'extracted_svgs')
    
    # 保存合并后的项目文件
    save_scratch_project(merged_project, output_path)
    
    print(f"合并后的项目文件已保存到: {output_path}")

if __name__ == "__main__":
    main()
