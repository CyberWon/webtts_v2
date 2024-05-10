from enum import Enum
from typing import Optional, Dict, Union, Annotated

from fastapi import Query
from pydantic import BaseModel


class SplitMethod(str, Enum):
    # cut0 = "不切"
    # cut1 = "凑4句一切"
    # cut2 = "凑50字一切"
    # cut3 = "中文句号。切"
    # cut4 = "英文句号.切"
    # cut5 = "按标点符号切"
    cut0 = "cut0"
    cut1 = "cut1"
    cut2 = "cut2"
    cut3 = "cut3"
    cut4 = "cut4"
    cut5 = "cut5"


class TextLang(str, Enum):
    # all_zh = "全中文"
    # en = "全英文"
    # all_ja = "全日文"
    # zh = "中英混合"
    # ja = "日英混合"
    # auto = "自动识别"
    all_zh = "all_zh"
    en = "en"
    all_ja = "all_ja"
    zh = "zh"
    ja = "ja"
    auto = "auto"


class AudioFormat(str, Enum):
    wav = "wav"
    mp3 = "mp3"
    ogg = "ogg"
    silk = "silk"


class Params(BaseModel):
    text: Union[str, None] = Query(None, description="文本内容", title="文本内容")
    spk: Union[str, None] = Query(
        None, description="发音人,不设置走默认的。", title="发音人"
    )
    emotion: Union[str, None] = Query(
        None, description="情感,不设置走默认的", title="情感"
    )
    speed: float = Query(1.0, description="语速", title="语速")
    format: AudioFormat = Query(
        AudioFormat.wav, description="输出文件格式", title="输出音频格式"
    )
    text_lang: TextLang = Query(TextLang.zh, description="文本语言", title="文本语言")
    batch_size: int = Query(1, description="分桶大小")
    text_split_method: SplitMethod = Query(
        SplitMethod.cut0,
        description="文本切割方式.cut0(不切),cut1(凑4句一切),cut2(凑50字一切),cut3(中文句号。切),cut4(英文句号.切),cut5(按标点符号切)",
    )
    temperature: float = Query(1, description="temperature")
    top_k: int = Query(20, description="top_k")
    top_p: float = Query(1, description="top_p")
    ref_wav_path: Union[str, None] = Query(
        None, description="参考音频路径,优先使用参数的"
    )

    prompt_text: Union[str, None] = Query(None, description="参考文本，优先使用参数的")
    prompt_language: Union[str, None] = Query(
        None, description="参考语言，优先使用参数的"
    )
    return_fragment: bool = Query(False, description="分段返回，默认不启用")
    fragment_interval: float = Query(0.3, description="分段时间间隔")
    seed: int = Query(-1, description="随机种子，-1为不固定")
    stream: bool = Query(False, description="是否为流式语音")


class VersionResp(BaseModel):
    version: str
    remote_version: dict


class Emotion(BaseModel):
    ref_wav_path: str
    text: str
    text_lang: str = "zh"


class Speaker(BaseModel):
    gpt_path: str
    ref_wav_path: str
    sovits_path: str
    text: str
    text_lang: str = "zh"
    emotion: Optional[Dict[str, Emotion]] = None


class AddModel(BaseModel):
    path: str
    save: Optional[bool] = False


class CommonResp(BaseModel):
    code: int = 200
    msg: str


class DeleteModel(BaseModel):
    name: str
    save: Optional[bool] = False
    all: Optional[bool] = False


class ConfigResp(BaseModel):
    default_speaker: Optional[str] = None
    keep_wav: bool = False
    tmp_dir: str = "tts_voice"
    server_host: str = "0.0.0.0"
    server_port: int = 8080
    public: Union[bool, int] = False
    model_dir: str = "models"
    is_half: bool = False
    domain: Optional[str] = ""
    device: str = "cpu"
    frp_adapter: Optional[str] = "gradio"
    frp_domain: Optional[str] = ""
    speaker: Optional[Dict[str, Speaker]] = None


class GroupVoicerEmo(BaseModel):
    top_p: int = Query(1, description="top_p")
    top_k: float = Query(20, description="top_k")
    temperature: float = Query(1, description="temperature")
    trial: str = Query("", description="试听音频")
    seed: int = Query(-1, description="随机种子")


class GroupVoicer(BaseModel):
    name: Optional[str] = Query("", description="发音人名称")
    code: Optional[str] = Query("", description="发音人代码")
    desc: Optional[str] = Query("", description="发音人描述")
    avatar: Optional[str] = Query("", description="发音人头像")


class VoicerGroup(BaseModel):
    name: str = Query("", description="发音人组名称")
