import os
import yaml
from pathlib import Path

def generate_yaml_config(audio_dir, output_yaml_path='/home/wangxiangbo0126/webMushra/configs/MOS_IterSE.yaml'):
    """
    生成语音质量主观评估的YAML配置文件
    
    参数:
    - audio_dir: 音频文件根目录，应包含10个cond子目录
    - output_yaml_path: 生成的YAML文件路径
    """
    # 验证输入目录是否存在
    audio_path = Path(audio_dir)
    if not audio_path.exists() or not audio_path.is_dir():
        raise ValueError(f"指定的音频目录不存在: {audio_dir}")
    
    # 获取所有cond目录（假设格式为cond1, cond2, ..., cond10）
    cond_dirs = sorted([d for d in audio_path.iterdir() if d.is_dir() and d.name.startswith('cond')])
    
    # 验证是否有10个cond目录
    if len(cond_dirs) != 10:
        raise ValueError(f"预期找到10个cond目录，但实际找到{len(cond_dirs)}个")
    
    # 分析第一个cond目录，获取样本列表（假设所有cond目录结构相同）
    sample_files = sorted([f.name for f in cond_dirs[0].iterdir() if f.is_file() and f.suffix.lower() in ['.wav', '.mp3']])
    
    # 生成YAML配置
    config = {
        'bufferSize': 2048,
        'language': 'cn',
        'pages': []
    }
    
    # 添加欢迎页
    config['pages'].append({
        'content': '欢迎来到语音增强质量的主观评测。<br>请单击 [下页] 按钮。',
        'id': 'welcome',
        'name': '语音增强质量评测',
        'type': 'generic'
    })
    
    # 添加说明页
    config['pages'].append({
        'content': '''分别播放“干净的”reference 和处理后的音频，然后以 reference 音频作为参照，对处理后的音频的质量进行打分（0 到 100之间）。<br><br><strong>注意：</strong>您可能需要为每个音频样本进行多个指标的打分，比如语音质量、背景噪声质量 和 整体音频质量。<br>语音质量 表示处理后的音频中<strong>语音信号</strong>的质量，<font color="red">而不关心背景噪声的部分</font>。<br>背景噪声质量 表示处理后的音频中<strong>背景噪声</strong>的质量，<font color="red">而不关心语音信号的部分</font>。<br>整体音频质量 表示处理后的音频的<strong>整体质量</strong>，即<font color="red">同时考虑语音和背景噪声</font>。<br><br><strong>在主观评测的过程中，直到测试结束之前，请不要关闭或重新加载此页面，否则进度将会丢失。</strong><br><br>请单击 [下页] 按钮。''',
        'id': 'explanation',
        'name': '测试介绍',
        'type': 'generic'
    })
    
    # 添加音量检查页（使用第一个样本的clean版本作为示例）
    config['pages'].append({
        'content': '这是和后面评测中您将听到的音频相似的一个语音样本。请根据它调整耳机的音量。<br><br><strong>在评测过程中，请使用耳机，并在相对安静的房间中进行听音。</strong>',
        'defaultVolume': 1.0,
        'id': 'volume_check',
        'stimulus': f'./configs/resources/samples/clean/{sample_files[0]}',
        'type': 'volume'
    })
    
    # 为每个cond和sample生成评测页
    for cond_idx, cond_dir in enumerate(cond_dirs, 1):
        cond_name = cond_dir.name
        
        for sample_idx, sample_file in enumerate(sample_files, 1):
            # 提取样本ID（不包含扩展名）
            sample_id = os.path.splitext(sample_file)[0]
            
            # 构建评测页配置
            eval_page = {
                'content': [
                    '分别播放 reference 和处理后的音频，然后对处理后的音频的<font color="red">整体质量</font>进行评估，即其中的语音信号是否很好地保留（无失真），同时背景噪声也被很好地抑制。<br>伴随着强干扰性噪声，且高度失真的语音，相应的得分是 0。几乎没有噪声，且无失真的语音，相应的得分是 100。<br><br><strong>注意：</strong>reference 音频可能也包含一定噪声，处理后的音频中如果噪声更小则更好。<br><br>',
                    '分别播放 reference 和处理后的音频，然后<strong>仅</strong>对处理后的音频中的<font color="red">语音质量</font>进行评估，即其中的语音信号是否很好地保留（无失真）。<br>高度失真的语音，相应的得分是 0。没有任何失真的语音，相应的得分是 100。<br><br><strong>注意：</strong>在评估 语音质量 分数时，请<u>不要将背景噪声考虑在内</u>。<br><br>',
                    '分别播放 reference 和处理后的音频，然后<strong>仅</strong>对处理后的音频中的<font color="red">噪声质量</font>进行评估，即其中的背景噪声的质量情况。<br>强干扰性噪声，相应的得分是 100。几乎无噪声，相应的得分是 0。<br><br><strong>注意(1)：</strong>在评估背景噪声质量 分数时，请<u>不要将语音信号的质量考虑在内</u>。<br><strong>注意(2)：</strong>请根据每段音频中噪声的<strong>相对于语音的音量</strong>（而非绝对音量）来对该样本进行打分，因为不同音频的绝对音量很可能是不完全相同的。'
                ],
                'createAnchor35': False,
                'createAnchor70': False,
                'enableLooping': True,
                'id': f'cond{cond_idx}_sample{sample_idx}',
                'metrics': [
                    '整体音频质量',
                    '语音质量',
                    '背景噪声质量'
                ],
                'mustPlayAll': True,
                'mustViewAllTabs': True,
                'name': f'语音增强质量评测 ({cond_idx}/10, {sample_idx}/{len(sample_files)})',
                'randomize': True,
                'reference': f'./configs/resources/samples/clean/{sample_file}',
                'response': [
                    ['很好', '好', '较好', '较差', '差'],
                    ['无失真', '轻微失真', '较失真', '相当失真', '极度失真'],
                    ['强干扰噪声', '有一定干扰性', '有噪声但无干扰性', '轻微噪声', '几乎无噪声']
                ],
                'showConditionNames': False,
                'stimuli': {
                    cond_name: f'./{cond_name}/{sample_file}'
                },
                'type': 'multi_metric_mushra'
            }
            
            config['pages'].append(eval_page)
    
    # 添加结束页
    config['pages'].append({
        'content': '评测结束，请输入您的<strong>名字</strong>，并单击 [提交结果] 按钮。',
        'id': 'finish',
        'name': '评测结束',
        'popupContent': '您的评测结果已被记录。感谢您的配合！',
        'questionnaire': [
            {
                'label': '名字',
                'name': 'name',
                'optional': False,
                'type': 'text'
            }
        ],
        'showResults': True,
        'type': 'finish',
        'writeResults': True
    })
    
    # 添加其他配置项
    config['remoteService'] = 'service/write.php'
    config['showButtonPreviousPage'] = True
    config['showWaveform'] = True
    config['stopOnErrors'] = True
    config['testId'] = 'subjective_evaluation'
    config['testname'] = 'Subjective evaluation of Speech Enhancement'
    
    # 写入YAML文件
    with open(output_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    
    print(f"YAML配置文件已生成: {output_yaml_path}")
    print(f"共生成 {len(config['pages'])} 个页面，包括 {len(sample_files) * len(cond_dirs)} 个评测项")
    
    return config

if __name__ == "__main__":
    # 用户需要修改此路径为实际音频目录
    audio_directory = "/home/wangxiangbo0126/webMushra/grouped_conditions"
    
    # 生成配置文件
    generate_yaml_config(audio_directory)