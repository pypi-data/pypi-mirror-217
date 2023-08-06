# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstackl_opy_ = 2048
bstack1l1_opy_ = 7
def bstack1l_opy_ (bstack1_opy_):
    global bstack11l_opy_
    stringNr = ord (bstack1_opy_ [-1])
    bstack1ll1_opy_ = bstack1_opy_ [:-1]
    bstack1ll_opy_ = stringNr % len (bstack1ll1_opy_)
    bstack1l1l_opy_ = bstack1ll1_opy_ [:bstack1ll_opy_] + bstack1ll1_opy_ [bstack1ll_opy_:]
    if bstack1lll_opy_:
        bstack11_opy_ = unicode () .join ([unichr (ord (char) - bstackl_opy_ - (bstack111_opy_ + stringNr) % bstack1l1_opy_) for bstack111_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11_opy_ = str () .join ([chr (ord (char) - bstackl_opy_ - (bstack111_opy_ + stringNr) % bstack1l1_opy_) for bstack111_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1l11ll1_opy_ = {
	bstack1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstack1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstack1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstack1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstack1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstack1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstack1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstack1l_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstack1l_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstack1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstack1l_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstack1l_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstack1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstack1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstack1l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstack1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstack1l_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstack1l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstack1l_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstack1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstack1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstack1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstack1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstack1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstack1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack11ll1_opy_ = [
  bstack1l_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstack1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstack1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack11l1ll1l_opy_ = {
  bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstack1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstack1l_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstack1l_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack11l1lll1l_opy_ = {
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack1l_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack11l1ll11_opy_ = {
  bstack1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack1l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack1l_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack1l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1l1111_opy_ = [
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack1l_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack1l_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack1l_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack1l_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack11111lll_opy_ = [
  bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack1lll1l11_opy_ = [
  bstack1l_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstack1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstack1l_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstack1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstack1l_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstack1l_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstack1l_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstack1l_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstack1l_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstack1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstack1l_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstack1l_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstack1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstack1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstack1l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstack1l_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstack1l_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstack1l_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstack1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstack1l_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstack1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstack1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstack1l_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstack1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstack1l_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstack1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstack1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstack1l_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstack1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstack1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstack1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstack1l_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstack1l_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstack1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstack1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstack1l_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstack1l_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstack1l_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack1l_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstack1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstack1l_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstack1l_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstack1l_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstack1l_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstack1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstack1l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstack1l_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstack1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstack1l_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstack1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstack1l_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstack1l_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstack1l_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstack1l_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstack1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstack1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstack1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstack1l_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstack1l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstack1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstack1l_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstack1l_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstack1l_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstack1l_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstack1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstack1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstack1l_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstack1l_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack11ll11l11_opy_ = {
  bstack1l_opy_ (u"࠭ࡶࠨच"): bstack1l_opy_ (u"ࠧࡷࠩछ"),
  bstack1l_opy_ (u"ࠨࡨࠪज"): bstack1l_opy_ (u"ࠩࡩࠫझ"),
  bstack1l_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstack1l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstack1l_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstack1l_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstack1l_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstack1l_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstack1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstack1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstack1l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstack1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstack1l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstack1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstack1l_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstack1l_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstack1l_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstack1l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstack1l_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstack1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstack1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstack1l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstack1l_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstack1l_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack11l1l_opy_ = bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1ll111_opy_ = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack11l111_opy_ = bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack1l1lll1ll_opy_ = {
  bstack1l_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack1l_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack1l_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1l11llll_opy_ = bstack1l1lll1ll_opy_[bstack1l_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack1lllll111_opy_ = bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1l1ll_opy_ = bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1llll11_opy_ = bstack1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1111111_opy_ = bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack1l1l11111_opy_ = [bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack1l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack11l1ll1_opy_ = [bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack1lll111ll_opy_ = [
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstack1l_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstack1l_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstack1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstack1l_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstack1l_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstack1l_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstack1l_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstack1l_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstack1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstack1l_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstack1l_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstack1l_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstack1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstack1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstack1l_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstack1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstack1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstack1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstack1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstack1l_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstack1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstack1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstack1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstack1l_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstack1l_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstack1l_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstack1l_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstack1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstack1l_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstack1l_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstack1l_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstack1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstack1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstack1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstack1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstack1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstack1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstack1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstack1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstack1l_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstack1l_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstack1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstack1l_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstack1l_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstack1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstack1l_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstack1l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstack1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstack1l_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstack1l_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstack1l_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstack1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstack1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstack1l_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstack1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstack1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstack1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstack1l_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstack1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstack1l_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstack1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstack1l_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstack1l_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstack1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstack1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstack1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstack1l_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstack1l_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstack1l_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstack1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstack1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstack1l_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstack1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstack1l_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstack1l_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstack1l_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstack1l_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstack1l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstack1l_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstack1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstack1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstack1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstack1l_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstack1l_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstack1l_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstack1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstack1l_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstack1l_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstack1l_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstack1l_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstack1l_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstack1l_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstack1l_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstack1l_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstack1l_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstack1l_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstack1l_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstack1l_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstack1l_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstack1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstack1l_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstack1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstack1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstack1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstack1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstack1l_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstack1l_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstack1l_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstack1l_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstack1l_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstack1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstack1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstack1l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstack1l_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstack1l_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstack1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack11111l1l_opy_ = bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack1111l11l_opy_ = [bstack1l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack1l_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack1l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1lll1l1_opy_ = [bstack1l_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack1l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1ll1l1l1_opy_ = {
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack1l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack1l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack111l111_opy_ = [
  bstack1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1l1l1l_opy_ = bstack11111lll_opy_ + bstack1lll1l11_opy_ + bstack1lll111ll_opy_
bstack1l11lll11_opy_ = [
  bstack1l_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack1l_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack1l_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack1l_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack1l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack1l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack1l_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack1ll1l1_opy_ = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack1ll1l1ll_opy_ = bstack1l_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack11lll111l_opy_ = [ bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack1lll11111_opy_ = [ bstack1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack1l111ll11_opy_ = [ bstack1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack11ll1l11l_opy_ = bstack1l_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack1llll1ll1_opy_ = bstack1l_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack11l111l_opy_ = bstack1l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1ll1111_opy_ = bstack1l_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack1l111111_opy_ = [
  bstack1l_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstack1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstack1l_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstack1l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstack1l_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstack1l_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstack1l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstack1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstack1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstack1l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstack1l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstack1l_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstack1l_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstack1l_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstack1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstack1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstack1l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstack1l_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstack1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstack1l_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstack1l_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
bstack1ll11l111_opy_ = bstack1l_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧਧ")
def bstack1l1ll1l_opy_():
  global CONFIG
  headers = {
        bstack1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਨ"): bstack1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ਩"),
      }
  proxy = bstack1ll1lll_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨਪ")) or CONFIG.get(bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪਫ")):
    proxies = {
      bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ਬ"): proxy
    }
  try:
    response = requests.get(bstack11l111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11lll1111_opy_ = response.json()[bstack1l_opy_ (u"ࠨࡪࡸࡦࡸ࠭ਭ")]
      logger.debug(bstack1ll1ll1ll_opy_.format(response.json()))
      return bstack11lll1111_opy_
    else:
      logger.debug(bstack11ll11ll_opy_.format(bstack1l_opy_ (u"ࠤࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡥࠡࡧࡵࡶࡴࡸࠠࠣਮ")))
  except Exception as e:
    logger.debug(bstack11ll11ll_opy_.format(e))
def bstack1l1111lll_opy_(hub_url):
  global CONFIG
  url = bstack1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧਯ")+  hub_url + bstack1l_opy_ (u"ࠦ࠴ࡩࡨࡦࡥ࡮ࠦਰ")
  headers = {
        bstack1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ਱"): bstack1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩਲ"),
      }
  proxy = bstack1ll1lll_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪਲ਼")) or CONFIG.get(bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ਴")):
    proxies = {
      bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨਵ"): proxy
    }
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1l111_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l11l1_opy_.format(hub_url, e))
def bstack1llllll1_opy_():
  try:
    global bstack1llll1l11_opy_
    bstack11lll1111_opy_ = bstack1l1ll1l_opy_()
    with Pool() as pool:
      results = pool.map(bstack1l1111lll_opy_, bstack11lll1111_opy_)
    bstack11ll11_opy_ = {}
    for item in results:
      hub_url = item[bstack1l_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫਸ਼")]
      latency = item[bstack1l_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬ਷")]
      bstack11ll11_opy_[hub_url] = latency
    bstack1l1lllll1_opy_ = min(bstack11ll11_opy_, key= lambda x: bstack11ll11_opy_[x])
    bstack1llll1l11_opy_ = bstack1l1lllll1_opy_
    logger.debug(bstack1lllll1_opy_.format(bstack1l1lllll1_opy_))
  except Exception as e:
    logger.debug(bstack1ll1l111l_opy_.format(e))
bstack1lll111l_opy_ = bstack1l_opy_ (u"࡙ࠬࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠻ࠢࡾࢁࠬਸ")
bstack1l1ll111l_opy_ = bstack1l_opy_ (u"࠭ࡃࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡶࡩࡹࡻࡰࠢࠩਹ")
bstack1llll1l1_opy_ = bstack1l_opy_ (u"ࠧࡑࡣࡵࡷࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩ਺")
bstack1ll1l1lll_opy_ = bstack1l_opy_ (u"ࠨࡕࡤࡲ࡮ࡺࡩࡻࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭਻")
bstack1ll11111_opy_ = bstack1l_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡪࡸࡦࠥࡻࡲ࡭࠼ࠣࡿࢂ਼࠭")
bstack111111_opy_ = bstack1l_opy_ (u"ࠪࡗࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࡼࡿࠪ਽")
bstack1ll11_opy_ = bstack1l_opy_ (u"ࠫࡗ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡩ࡯ࡶࡨࡶࡷࡻࡰࡵ࠮ࠣࡩࡽ࡯ࡴࡪࡰࡪࠫਾ")
bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪਿ")
bstack1l11lll1_opy_ = bstack1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡢࡰࡧࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫੀ")
bstack1l1ll11l1_opy_ = bstack1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡴࡲࡦࡴࡺࠬࠡࡲࡤࡦࡴࡺࠠࡢࡰࡧࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡲࡩࡣࡴࡤࡶࡾࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡶࡲࠤࡷࡻ࡮ࠡࡴࡲࡦࡴࡺࠠࡵࡧࡶࡸࡸࠦࡩ࡯ࠢࡳࡥࡷࡧ࡬࡭ࡧ࡯࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠳ࡰࡢࡤࡲࡸࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࡡࠩੁ")
bstack1ll111l11_opy_ = bstack1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡥࡩ࡭ࡧࡶࡦࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࡡࠩੂ")
bstack1l1l11ll_opy_ = bstack1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡥࡵࡶࡩࡶ࡯࠰ࡧࡱ࡯ࡥ࡯ࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡄࡴࡵ࡯ࡵ࡮࠯ࡓࡽࡹ࡮࡯࡯࠯ࡆࡰ࡮࡫࡮ࡵࡢࠪ੃")
bstack11l1l1l1l_opy_ = bstack1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡤࠬ੄")
bstack1l1ll1ll_opy_ = bstack1l_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡧ࡫ࡱࡨࠥ࡫ࡩࡵࡪࡨࡶ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡰࡴࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡷࡥࡱࡲࠠࡵࡪࡨࠤࡷ࡫࡬ࡦࡸࡤࡲࡹࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡷࡶ࡭ࡳ࡭ࠠࡱ࡫ࡳࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠫ੅")
bstack1lll11l11_opy_ = bstack1l_opy_ (u"ࠬࡎࡡ࡯ࡦ࡯࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥ࡯ࡳࡸ࡫ࠧ੆")
bstack11ll11ll1_opy_ = bstack1l_opy_ (u"࠭ࡁ࡭࡮ࠣࡨࡴࡴࡥࠢࠩੇ")
bstack1l1ll1lll_opy_ = bstack1l_opy_ (u"ࠧࡄࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࠦࡡࡵࠢࡤࡲࡾࠦࡰࡢࡴࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡲࡪࠥࠨࡻࡾࠤ࠱ࠤࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡧࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮࠲ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠠࡧ࡫࡯ࡩࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡴࡦࡵࡷࡷ࠳࠭ੈ")
bstack11l11ll1_opy_ = bstack1l_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡴࡨࡨࡪࡴࡴࡪࡣ࡯ࡷࠥࡴ࡯ࡵࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡷ࡬ࡪࡳࠠࡪࡰࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡦࡹࠠࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥࠤࡦࡴࡤࠡࠤࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠧࠦ࡯ࡳࠢࡶࡩࡹࠦࡴࡩࡧࡰࠤࡦࡹࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳ࠻ࠢࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦࠥࡧ࡮ࡥࠢࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞ࠨࠧ੉")
bstack1l1l1l111_opy_ = bstack1l_opy_ (u"ࠩࡐࡥࡱ࡬࡯ࡳ࡯ࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠦࢀࢃࠢࠨ੊")
bstack11l1llll_opy_ = bstack1l_opy_ (u"ࠪࡉࡳࡩ࡯ࡶࡰࡷࡩࡷ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣ࠱ࠥࢁࡽࠨੋ")
bstack11l1l1ll_opy_ = bstack1l_opy_ (u"ࠫࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫੌ")
bstack11llllll_opy_ = bstack1l_opy_ (u"࡙ࠬࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰ੍ࠬ")
bstack1l111111l_opy_ = bstack1l_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠤ࡮ࡹࠠ࡯ࡱࡺࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠦ࠭੎")
bstack1l11_opy_ = bstack1l_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲ࠺ࠡࡽࢀࠫ੏")
bstack1ll11111l_opy_ = bstack1l_opy_ (u"ࠨࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡥ࡭ࡳࡧࡲࡺࠢࡺ࡭ࡹ࡮ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࡾࢁࠬ੐")
bstack1ll11l1_opy_ = bstack1l_opy_ (u"ࠩࡘࡴࡩࡧࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪੑ")
bstack111ll1_opy_ = bstack1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠩ੒")
bstack1l1l1l11l_opy_ = bstack1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࠥࡧ࡮ࠡࡣࡳࡴࡷࡵࡰࡳ࡫ࡤࡸࡪࠦࡆࡘࠢࠫࡶࡴࡨ࡯ࡵ࠱ࡳࡥࡧࡵࡴࠪࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠯ࠤࡸࡱࡩࡱࠢࡷ࡬ࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡮ࡩࡾࠦࡩ࡯ࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡪࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡳࡪ࡯ࡳࡰࡪࠦࡰࡺࡶ࡫ࡳࡳࠦࡳࡤࡴ࡬ࡴࡹࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡢࡰࡼࠤࡋ࡝࠮ࠨ੓")
bstack11ll1lll_opy_ = bstack1l_opy_ (u"࡙ࠬࡥࡵࡶ࡬ࡲ࡬ࠦࡨࡵࡶࡳࡔࡷࡵࡸࡺ࠱࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡩࡵࡳࡴࡨࡲࡹࡲࡹࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࠬࢀࢃࠩ࠭ࠢࡳࡰࡪࡧࡳࡦࠢࡸࡴ࡬ࡸࡡࡥࡧࠣࡸࡴࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭࠿࠿࠷࠲࠵࠴࠰ࠡࡱࡵࠤࡷ࡫ࡦࡦࡴࠣࡸࡴࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠱ࡵࡹࡳ࠳ࡴࡦࡵࡷࡷ࠲ࡨࡥࡩ࡫ࡱࡨ࠲ࡶࡲࡰࡺࡼࠧࡵࡿࡴࡩࡱࡱࠤ࡫ࡵࡲࠡࡣࠣࡻࡴࡸ࡫ࡢࡴࡲࡹࡳࡪ࠮ࠨ੔")
bstack11llllll1_opy_ = bstack1l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲࠳࠭੕")
bstack1l1l1l1ll_opy_ = bstack1l_opy_ (u"ࠧࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡧࡦࡰࡨࡶࡦࡺࡥࡥࠢࡷ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠥࠬ੖")
bstack11lll111_opy_ = bstack1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫࠮ࠡࡽࢀࠫ੗")
bstack111l1111_opy_ = bstack1l_opy_ (u"ࠩࡈࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡺࠠ࡭ࡧࡤࡷࡹࠦ࠱ࠡ࡫ࡱࡴࡺࡺࠬࠡࡴࡨࡧࡪ࡯ࡶࡦࡦࠣ࠴ࠬ੘")
bstack1ll11ll11_opy_ = bstack1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡹࡷ࡯࡮ࡨࠢࡄࡴࡵࠦࡵࡱ࡮ࡲࡥࡩ࠴ࠠࡼࡿࠪਖ਼")
bstack11l111l1_opy_ = bstack1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲ࡯ࡳࡦࡪࠠࡂࡲࡳ࠲ࠥࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࢀࢃ࠮ࠨਗ਼")
bstack1llll_opy_ = bstack1l_opy_ (u"ࠬࡑࡥࡺࡵࠣࡧࡦࡴ࡮ࡰࡶࠣࡧࡴ࠳ࡥࡹ࡫ࡶࡸࠥࡧࡳࠡࡣࡳࡴࠥࡼࡡ࡭ࡷࡨࡷ࠱ࠦࡵࡴࡧࠣࡥࡳࡿࠠࡰࡰࡨࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࠦࡦࡳࡱࡰࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠮ࠣࡳࡳࡲࡹࠡࠤࡳࡥࡹ࡮ࠢࠡࡣࡱࡨࠥࠨࡣࡶࡵࡷࡳࡲࡥࡩࡥࠤࠣࡧࡦࡴࠠࡤࡱ࠰ࡩࡽ࡯ࡳࡵࠢࡷࡳ࡬࡫ࡴࡩࡧࡵ࠲ࠬਜ਼")
bstack1llll1111_opy_ = bstack1l_opy_ (u"࡛࠭ࡊࡰࡹࡥࡱ࡯ࡤࠡࡣࡳࡴࠥࡶࡲࡰࡲࡨࡶࡹࡿ࡝ࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠡࡣࡵࡩࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠱ࠤࡋࡵࡲࠡ࡯ࡲࡶࡪࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡱ࡮ࡨࡥࡸ࡫ࠠࡷ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡰࡪࡷࡰ࠳ࡸ࡫ࡴ࠮ࡷࡳ࠱ࡹ࡫ࡳࡵࡵ࠲ࡷࡵ࡫ࡣࡪࡨࡼ࠱ࡦࡶࡰࠨੜ")
bstack1111l1l_opy_ = bstack1l_opy_ (u"ࠧ࡜ࡋࡱࡺࡦࡲࡩࡥࠢࡤࡴࡵࠦࡰࡳࡱࡳࡩࡷࡺࡹ࡞ࠢࡖࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࡷࠥࡵࡦࠡࡣࡳࡴࠥࡧࡲࡦࠢࡲࡪࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠱ࠤࡋࡵࡲࠡ࡯ࡲࡶࡪࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡱ࡮ࡨࡥࡸ࡫ࠠࡷ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡰࡪࡷࡰ࠳ࡸ࡫ࡴ࠮ࡷࡳ࠱ࡹ࡫ࡳࡵࡵ࠲ࡷࡵ࡫ࡣࡪࡨࡼ࠱ࡦࡶࡰࠨ੝")
bstack11l1111l_opy_ = bstack1l_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡤࡴࡵࠦࡩࡥࠢࡾࢁࠥ࡬࡯ࡳࠢ࡫ࡥࡸ࡮ࠠ࠻ࠢࡾࢁ࠳࠭ਫ਼")
bstack11ll1l1_opy_ = bstack1l_opy_ (u"ࠩࡄࡴࡵࠦࡕࡱ࡮ࡲࡥࡩ࡫ࡤࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠡࡋࡇࠤ࠿ࠦࡻࡾࠩ੟")
bstack11111l1_opy_ = bstack1l_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡄࡴࡵࠦ࠺ࠡࡽࢀ࠲ࠬ੠")
bstack1lll1l11l_opy_ = bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡱࡵࠤࡻࡧ࡮ࡪ࡮࡯ࡥࠥࡶࡹࡵࡪࡲࡲࠥࡺࡥࡴࡶࡶ࠰ࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡵࡧࡲࡢ࡮࡯ࡩࡱࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡁࠥ࠷ࠧ੡")
bstack1111ll11_opy_ = bstack1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࠾ࠥࢁࡽࠨ੢")
bstack111l11l_opy_ = bstack1l_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡦࡰࡴࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳ࠼ࠣࡿࢂ࠭੣")
bstack11lll11_opy_ = bstack1l_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣ࡫ࡪࡺࠠࡳࡧࡤࡷࡴࡴࠠࡧࡱࡵࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪ࠴ࠠࡼࡿࠪ੤")
bstack111l1ll_opy_ = bstack1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡢࡲ࡬ࠤࡨࡧ࡬࡭࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭੥")
bstack1l11lll_opy_ = bstack1l_opy_ (u"ࠩࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡨࡰࡹࠣࡦࡺ࡯࡬ࡥࠢࡘࡖࡑ࠲ࠠࡢࡵࠣࡦࡺ࡯࡬ࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾࠦࡩࡴࠢࡱࡳࡹࠦࡵࡴࡧࡧ࠲ࠬ੦")
bstack11ll111l_opy_ = bstack1l_opy_ (u"ࠪࡗࡪࡸࡶࡦࡴࠣࡷ࡮ࡪࡥࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠬࢀࢃࠩࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡤࡱࡪࠦࡡࡴࠢࡦࡰ࡮࡫࡮ࡵࠢࡶ࡭ࡩ࡫ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠫࡿࢂ࠯ࠧ੧")
bstack11l111ll_opy_ = bstack1l_opy_ (u"࡛ࠫ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡨࡦࡹࡨࡣࡱࡤࡶࡩࡀࠠࡼࡿࠪ੨")
bstack1lll1ll_opy_ = bstack1l_opy_ (u"࡛ࠬ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡣࡦࡧࡪࡹࡳࠡࡣࠣࡴࡷ࡯ࡶࡢࡶࡨࠤࡩࡵ࡭ࡢ࡫ࡱ࠾ࠥࢁࡽࠡ࠰ࠣࡗࡪࡺࠠࡵࡪࡨࠤ࡫ࡵ࡬࡭ࡱࡺ࡭ࡳ࡭ࠠࡤࡱࡱࡪ࡮࡭ࠠࡪࡰࠣࡽࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠼ࠣࡠࡳ࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯ࠣࡠࡳࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮࠽ࠤࡹࡸࡵࡦࠢ࡟ࡲ࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮ࠩ੩")
bstack1l1l1llll_opy_ = bstack1l_opy_ (u"࠭ࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࡢࡩࡷࡸ࡯ࡳࠢ࠽ࠤࢀࢃࠧ੪")
bstack1l1lll11_opy_ = bstack1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡳࡪ࡟ࡢ࡯ࡳࡰ࡮ࡺࡵࡥࡧࡢࡩࡻ࡫࡮ࡵࠢࡩࡳࡷࠦࡓࡅࡍࡖࡩࡹࡻࡰࠡࡽࢀࠦ੫")
bstack1l11l1ll_opy_ = bstack1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠣࡿࢂࠨ੬")
bstack1lll1llll_opy_ = bstack1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠥࢁࡽࠣ੭")
bstack11llll111_opy_ = bstack1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬ࡩࡳࡧࡢࡶࡪࡷࡵࡦࡵࡷࠤࢀࢃࠢ੮")
bstack11l1l1l11_opy_ = bstack1l_opy_ (u"ࠦࡕࡕࡓࡕࠢࡈࡺࡪࡴࡴࠡࡽࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦ࠺ࠡࡽࢀࠦ੯")
bstack1ll111l1_opy_ = bstack1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡵࡸ࡯ࡹࡻࠣࡷࡪࡺࡴࡪࡰࡪࡷ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩੰ")
bstack1ll1ll1ll_opy_ = bstack1l_opy_ (u"࠭ࡒࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦ࠯࡯ࡧࡻࡸࡤ࡮ࡵࡣࡵࠣࡿࢂ࠭ੱ")
bstack11ll11ll_opy_ = bstack1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣ࠳ࡳ࡫ࡸࡵࡡ࡫ࡹࡧࡹ࠺ࠡࡽࢀࠫੲ")
bstack1lllll1_opy_ = bstack1l_opy_ (u"ࠨࡐࡨࡥࡷ࡫ࡳࡵࠢ࡫ࡹࡧࠦࡡ࡭࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡷ࠿ࠦࡻࡾࠩੳ")
bstack1ll1l111l_opy_ = bstack1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࠡࡋࡑࠤࡆࡒࡌࡐࡅࡄࡘࡊࠦࡈࡖࡄࠣࡿࢂ࠭ੴ")
bstack1ll1l111_opy_ = bstack1l_opy_ (u"ࠪࡐࡦࡺࡥ࡯ࡥࡼࠤࡴ࡬ࠠࡩࡷࡥ࠾ࠥࢁࡽࠡ࡫ࡶ࠾ࠥࢁࡽࠨੵ")
bstack11l11l1_opy_ = bstack1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠ࡭ࡣࡷࡩࡳࡩࡹࠡࡨࡲࡶࠥࢁࡽࠡࡪࡸࡦ࠿ࠦࡻࡾࠩ੶")
bstack1l111l11_opy_ = bstack1l_opy_ (u"ࠬࡎࡵࡣࠢࡸࡶࡱࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡰࡲࡷ࡭ࡲࡧ࡬ࠡࡪࡸࡦ࠿ࠦࡻࡾࠩ੷")
bstack1ll111l_opy_ = bstack1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡲࡴࡹ࡯࡭ࡢ࡮ࠣ࡬ࡺࡨࠠࡶࡴ࡯࠾ࠥࢁࡽࠨ੸")
bstack1111lll1_opy_ = bstack1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡮࡬ࡷࡹࡹ࠺ࠡࡽࢀࠫ੹")
bstack1ll111ll_opy_ = bstack1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠺ࠡࡽࢀࠫ੺")
bstack1l11l_opy_ = bstack1l_opy_ (u"ࠩࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠢࠣ࡭࡫࠮ࡰࡢࡩࡨࠤࡂࡃ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠢࡾࡠࡳࠦࠠࠡࡶࡵࡽࢀࡢ࡮ࠡࡥࡲࡲࡸࡺࠠࡧࡵࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮࡜ࠨࡨࡶࡠࠬ࠯࠻࡝ࡰࠣࠤࠥࠦࠠࡧࡵ࠱ࡥࡵࡶࡥ࡯ࡦࡉ࡭ࡱ࡫ࡓࡺࡰࡦࠬࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩ࠮ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡵࡥࡩ࡯ࡦࡨࡼ࠮ࠦࠫࠡࠤ࠽ࠦࠥ࠱ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭࠮ࡡࡸࡣ࡬ࡸࠥࡴࡥࡸࡒࡤ࡫ࡪ࠸࠮ࡦࡸࡤࡰࡺࡧࡴࡦࠪࠥࠬ࠮ࠦ࠽࠿ࠢࡾࢁࠧ࠲ࠠ࡝ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠨࡽ࡝ࠩࠬ࠭࠮ࡡࠢࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠥࡡ࠮ࠦࠫࠡࠤ࠯ࡠࡡࡴࠢࠪ࡞ࡱࠤࠥࠦࠠࡾࡥࡤࡸࡨ࡮ࠨࡦࡺࠬࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡿ࡟ࡲࠥࠦ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠩ੻")
bstack111ll1ll_opy_ = bstack1l_opy_ (u"ࠪࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡢ࡮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡢ࡮ࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻࡝ࡰ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰࡯ࡥࡺࡴࡣࡩࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶ࠭ࠥࡃ࠾ࠡࡽ࡟ࡲࡱ࡫ࡴࠡࡥࡤࡴࡸࡁ࡜࡯ࡶࡵࡽࠥࢁ࡜࡯ࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࢃ࡜࡯ࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶࠫࡿࡡࡴࠠࠡࠢࠣࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺ࠺ࠡࡢࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠨࢀ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬࢁࡥ࠲࡜࡯ࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩ੼")
from ._version import __version__
bstack1l1ll1ll1_opy_ = None
CONFIG = {}
bstack1l1l1l1_opy_ = {}
bstack1l1ll11l_opy_ = {}
bstack1l1l11lll_opy_ = None
bstack11l1l11l1_opy_ = None
bstack1l1llll1_opy_ = None
bstack1l1l1lll1_opy_ = -1
bstack111ll111_opy_ = bstack1l11llll_opy_
bstack1l111ll1l_opy_ = 1
bstack1l11l111_opy_ = False
bstack1llllllll_opy_ = bstack1l_opy_ (u"ࠫࠬ੽")
bstack1ll1l_opy_ = bstack1l_opy_ (u"ࠬ࠭੾")
bstack1lll1ll1_opy_ = False
bstack11lll1_opy_ = True
bstack1l11ll_opy_ = bstack1l_opy_ (u"࠭ࠧ੿")
bstack1l1ll1_opy_ = []
bstack1llll1l11_opy_ = bstack1l_opy_ (u"ࠧࠨ઀")
bstack1l11111_opy_ = False
bstack111l1l_opy_ = None
bstack1l111l111_opy_ = -1
bstack1lllll11_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪઁ")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩં"), bstack1l_opy_ (u"ࠪ࠲ࡷࡵࡢࡰࡶ࠰ࡶࡪࡶ࡯ࡳࡶ࠰࡬ࡪࡲࡰࡦࡴ࠱࡮ࡸࡵ࡮ࠨઃ"))
bstack1111l11_opy_ = False
bstack1l111l_opy_ = None
bstack1l1l1ll_opy_ = None
bstack1ll11l11_opy_ = None
bstack1llll111l_opy_ = None
bstack11lllll1_opy_ = None
bstack11lll1l1l_opy_ = None
bstack11llll11l_opy_ = None
bstack111ll1l_opy_ = None
bstack1l11lllll_opy_ = None
bstack1l1ll11_opy_ = None
bstack1ll11l1l1_opy_ = None
bstack1l1l11ll1_opy_ = None
bstack1l1l1ll1l_opy_ = None
bstack11l11_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack1lllllll1_opy_ = bstack1l_opy_ (u"ࠦࠧ઄")
class bstack1l1l1111_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1l1l1111_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack111ll111_opy_,
                    format=bstack1l_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪઅ"),
                    datefmt=bstack1l_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨઆ"))
def bstack11ll11111_opy_():
  global CONFIG
  global bstack111ll111_opy_
  if bstack1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩઇ") in CONFIG:
    bstack111ll111_opy_ = bstack1l1lll1ll_opy_[CONFIG[bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪઈ")]]
    logging.getLogger().setLevel(bstack111ll111_opy_)
def bstack11lllll_opy_():
  global CONFIG
  global bstack1111l11_opy_
  bstack11l1lll11_opy_ = bstack1l1lll1l_opy_(CONFIG)
  if(bstack1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫઉ") in bstack11l1lll11_opy_ and str(bstack11l1lll11_opy_[bstack1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઊ")]).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩઋ")):
    bstack1111l11_opy_ = True
def bstack1l11lll1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11lll1ll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll1l111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤઌ") == args[i].lower() or bstack1l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢઍ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l11ll_opy_
      bstack1l11ll_opy_ += bstack1l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ઎") + path
      return path
  return None
def bstack1llll1_opy_():
  bstack1l11l1l_opy_ = bstack11ll1l111_opy_()
  if bstack1l11l1l_opy_ and os.path.exists(os.path.abspath(bstack1l11l1l_opy_)):
    fileName = bstack1l11l1l_opy_
  if bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬએ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ઐ")])) and not bstack1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬઑ") in locals():
    fileName = os.environ[bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ઒")]
  if bstack1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧઓ") in locals():
    bstack1ll11lll1_opy_ = os.path.abspath(fileName)
  else:
    bstack1ll11lll1_opy_ = bstack1l_opy_ (u"࠭ࠧઔ")
  bstack1l111ll_opy_ = os.getcwd()
  bstack1llll11ll_opy_ = bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪક")
  bstack1l1llllll_opy_ = bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬખ")
  while (not os.path.exists(bstack1ll11lll1_opy_)) and bstack1l111ll_opy_ != bstack1l_opy_ (u"ࠤࠥગ"):
    bstack1ll11lll1_opy_ = os.path.join(bstack1l111ll_opy_, bstack1llll11ll_opy_)
    if not os.path.exists(bstack1ll11lll1_opy_):
      bstack1ll11lll1_opy_ = os.path.join(bstack1l111ll_opy_, bstack1l1llllll_opy_)
    if bstack1l111ll_opy_ != os.path.dirname(bstack1l111ll_opy_):
      bstack1l111ll_opy_ = os.path.dirname(bstack1l111ll_opy_)
    else:
      bstack1l111ll_opy_ = bstack1l_opy_ (u"ࠥࠦઘ")
  if not os.path.exists(bstack1ll11lll1_opy_):
    bstack1l111llll_opy_(
      bstack1l1ll1lll_opy_.format(os.getcwd()))
  with open(bstack1ll11lll1_opy_, bstack1l_opy_ (u"ࠫࡷ࠭ઙ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l111llll_opy_(bstack1l1l1l111_opy_.format(str(exc)))
def bstack1l11111l1_opy_(config):
  bstack1ll1lll11_opy_ = bstack1l111_opy_(config)
  for option in list(bstack1ll1lll11_opy_):
    if option.lower() in bstack11ll11l11_opy_ and option != bstack11ll11l11_opy_[option.lower()]:
      bstack1ll1lll11_opy_[bstack11ll11l11_opy_[option.lower()]] = bstack1ll1lll11_opy_[option]
      del bstack1ll1lll11_opy_[option]
  return config
def bstack11ll11l1_opy_():
  global bstack1l1ll11l_opy_
  for key, bstack11l1l1lll_opy_ in bstack11l1ll1l_opy_.items():
    if isinstance(bstack11l1l1lll_opy_, list):
      for var in bstack11l1l1lll_opy_:
        if var in os.environ:
          bstack1l1ll11l_opy_[key] = os.environ[var]
          break
    elif bstack11l1l1lll_opy_ in os.environ:
      bstack1l1ll11l_opy_[key] = os.environ[bstack11l1l1lll_opy_]
  if bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧચ") in os.environ:
    bstack1l1ll11l_opy_[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪછ")] = {}
    bstack1l1ll11l_opy_[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫજ")][bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪઝ")] = os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫઞ")]
def bstack11ll1l_opy_():
  global bstack1l1l1l1_opy_
  global bstack1l11ll_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1l_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ટ").lower() == val.lower():
      bstack1l1l1l1_opy_[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨઠ")] = {}
      bstack1l1l1l1_opy_[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩડ")][bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨઢ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1llll1lll_opy_ in bstack11l1lll1l_opy_.items():
    if isinstance(bstack1llll1lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1llll1lll_opy_:
          if idx<len(sys.argv) and bstack1l_opy_ (u"ࠧ࠮࠯ࠪણ") + var.lower() == val.lower() and not key in bstack1l1l1l1_opy_:
            bstack1l1l1l1_opy_[key] = sys.argv[idx+1]
            bstack1l11ll_opy_ += bstack1l_opy_ (u"ࠨࠢ࠰࠱ࠬત") + var + bstack1l_opy_ (u"ࠩࠣࠫથ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1l_opy_ (u"ࠪ࠱࠲࠭દ") + bstack1llll1lll_opy_.lower() == val.lower() and not key in bstack1l1l1l1_opy_:
          bstack1l1l1l1_opy_[key] = sys.argv[idx+1]
          bstack1l11ll_opy_ += bstack1l_opy_ (u"ࠫࠥ࠳࠭ࠨધ") + bstack1llll1lll_opy_ + bstack1l_opy_ (u"ࠬࠦࠧન") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack11ll1l1ll_opy_(config):
  bstack1ll1ll111_opy_ = config.keys()
  for bstack1ll11l_opy_, bstack1l111l1ll_opy_ in bstack1l11ll1_opy_.items():
    if bstack1l111l1ll_opy_ in bstack1ll1ll111_opy_:
      config[bstack1ll11l_opy_] = config[bstack1l111l1ll_opy_]
      del config[bstack1l111l1ll_opy_]
  for bstack1ll11l_opy_, bstack1l111l1ll_opy_ in bstack11l1ll11_opy_.items():
    if isinstance(bstack1l111l1ll_opy_, list):
      for bstack1ll1l1111_opy_ in bstack1l111l1ll_opy_:
        if bstack1ll1l1111_opy_ in bstack1ll1ll111_opy_:
          config[bstack1ll11l_opy_] = config[bstack1ll1l1111_opy_]
          del config[bstack1ll1l1111_opy_]
          break
    elif bstack1l111l1ll_opy_ in bstack1ll1ll111_opy_:
        config[bstack1ll11l_opy_] = config[bstack1l111l1ll_opy_]
        del config[bstack1l111l1ll_opy_]
  for bstack1ll1l1111_opy_ in list(config):
    for bstack11ll1l1l_opy_ in bstack1l1l1l_opy_:
      if bstack1ll1l1111_opy_.lower() == bstack11ll1l1l_opy_.lower() and bstack1ll1l1111_opy_ != bstack11ll1l1l_opy_:
        config[bstack11ll1l1l_opy_] = config[bstack1ll1l1111_opy_]
        del config[bstack1ll1l1111_opy_]
  bstack11ll11l1l_opy_ = []
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ઩") in config:
    bstack11ll11l1l_opy_ = config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪપ")]
  for platform in bstack11ll11l1l_opy_:
    for bstack1ll1l1111_opy_ in list(platform):
      for bstack11ll1l1l_opy_ in bstack1l1l1l_opy_:
        if bstack1ll1l1111_opy_.lower() == bstack11ll1l1l_opy_.lower() and bstack1ll1l1111_opy_ != bstack11ll1l1l_opy_:
          platform[bstack11ll1l1l_opy_] = platform[bstack1ll1l1111_opy_]
          del platform[bstack1ll1l1111_opy_]
  for bstack1ll11l_opy_, bstack1l111l1ll_opy_ in bstack11l1ll11_opy_.items():
    for platform in bstack11ll11l1l_opy_:
      if isinstance(bstack1l111l1ll_opy_, list):
        for bstack1ll1l1111_opy_ in bstack1l111l1ll_opy_:
          if bstack1ll1l1111_opy_ in platform:
            platform[bstack1ll11l_opy_] = platform[bstack1ll1l1111_opy_]
            del platform[bstack1ll1l1111_opy_]
            break
      elif bstack1l111l1ll_opy_ in platform:
        platform[bstack1ll11l_opy_] = platform[bstack1l111l1ll_opy_]
        del platform[bstack1l111l1ll_opy_]
  for bstack1ll1ll1l_opy_ in bstack1ll1l1l1_opy_:
    if bstack1ll1ll1l_opy_ in config:
      if not bstack1ll1l1l1_opy_[bstack1ll1ll1l_opy_] in config:
        config[bstack1ll1l1l1_opy_[bstack1ll1ll1l_opy_]] = {}
      config[bstack1ll1l1l1_opy_[bstack1ll1ll1l_opy_]].update(config[bstack1ll1ll1l_opy_])
      del config[bstack1ll1ll1l_opy_]
  for platform in bstack11ll11l1l_opy_:
    for bstack1ll1ll1l_opy_ in bstack1ll1l1l1_opy_:
      if bstack1ll1ll1l_opy_ in list(platform):
        if not bstack1ll1l1l1_opy_[bstack1ll1ll1l_opy_] in platform:
          platform[bstack1ll1l1l1_opy_[bstack1ll1ll1l_opy_]] = {}
        platform[bstack1ll1l1l1_opy_[bstack1ll1ll1l_opy_]].update(platform[bstack1ll1ll1l_opy_])
        del platform[bstack1ll1ll1l_opy_]
  config = bstack1l11111l1_opy_(config)
  return config
def bstack11llll1_opy_(config):
  global bstack1ll1l_opy_
  if bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬફ") in config and str(config[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭બ")]).lower() != bstack1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩભ"):
    if not bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨમ") in config:
      config[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩય")] = {}
    if not bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨર") in config[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")]:
      bstack1l11llll1_opy_ = datetime.datetime.now()
      bstack111ll1l1_opy_ = bstack1l11llll1_opy_.strftime(bstack1l_opy_ (u"ࠨࠧࡧࡣࠪࡨ࡟ࠦࡊࠨࡑࠬલ"))
      hostname = socket.gethostname()
      bstack1llll111_opy_ = bstack1l_opy_ (u"ࠩࠪળ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l_opy_ (u"ࠪࡿࢂࡥࡻࡾࡡࡾࢁࠬ઴").format(bstack111ll1l1_opy_, hostname, bstack1llll111_opy_)
      config[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨવ")][bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧશ")] = identifier
    bstack1ll1l_opy_ = config[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪષ")][bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩસ")]
  return config
def bstack1l11ll1ll_opy_():
  if (
    isinstance(os.getenv(bstack1l_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑ࠭હ")), str) and len(os.getenv(bstack1l_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠧ઺"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠩ઻")), str) and len(os.getenv(bstack1l_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇ઼ࠪ"))) > 0
  ):
    return os.getenv(bstack1l_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫઽ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"࠭ࡃࡊࠩા"))).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬિ") and str(os.getenv(bstack1l_opy_ (u"ࠨࡅࡌࡖࡈࡒࡅࡄࡋࠪી"))).lower() == bstack1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧુ"):
    return os.getenv(bstack1l_opy_ (u"ࠪࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒ࠭ૂ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠫࡈࡏࠧૃ"))).lower() == bstack1l_opy_ (u"ࠬࡺࡲࡶࡧࠪૄ") and str(os.getenv(bstack1l_opy_ (u"࠭ࡔࡓࡃ࡙ࡍࡘ࠭ૅ"))).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ૆"):
    return os.getenv(bstack1l_opy_ (u"ࠨࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧે"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠩࡆࡍࠬૈ"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨૉ") and str(os.getenv(bstack1l_opy_ (u"ࠫࡈࡏ࡟ࡏࡃࡐࡉࠬ૊"))).lower() == bstack1l_opy_ (u"ࠬࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠧો"):
    return 0 # bstack11lll1ll_opy_ bstack1l1lll1_opy_ not set build number env
  if os.getenv(bstack1l_opy_ (u"࠭ࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠩૌ")) and os.getenv(bstack1l_opy_ (u"ࠧࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖ્ࠪ")):
    return os.getenv(bstack1l_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪ૎"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠩࡆࡍࠬ૏"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨૐ") and str(os.getenv(bstack1l_opy_ (u"ࠫࡉࡘࡏࡏࡇࠪ૑"))).lower() == bstack1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ૒"):
    return os.getenv(bstack1l_opy_ (u"࠭ࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫ૓"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠧࡄࡋࠪ૔"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭૕") and str(os.getenv(bstack1l_opy_ (u"ࠩࡖࡉࡒࡇࡐࡉࡑࡕࡉࠬ૖"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ૗"):
    return os.getenv(bstack1l_opy_ (u"ࠫࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠧ૘"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠬࡉࡉࠨ૙"))).lower() == bstack1l_opy_ (u"࠭ࡴࡳࡷࡨࠫ૚") and str(os.getenv(bstack1l_opy_ (u"ࠧࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠪ૛"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭૜"):
    return os.getenv(bstack1l_opy_ (u"ࠩࡆࡍࡤࡐࡏࡃࡡࡌࡈࠬ૝"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠪࡇࡎ࠭૞"))).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ૟") and str(os.getenv(bstack1l_opy_ (u"ࠬࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠨૠ"))).lower() == bstack1l_opy_ (u"࠭ࡴࡳࡷࡨࠫૡ"):
    return os.getenv(bstack1l_opy_ (u"ࠧࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩૢ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠨࡖࡉࡣࡇ࡛ࡉࡍࡆࠪૣ"))).lower() == bstack1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૤"):
    return os.getenv(bstack1l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪ૥"), 0)
  return -1
def bstack11ll11lll_opy_(bstack1lll111_opy_):
  global CONFIG
  if not bstack1l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭૦") in CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૧")]:
    return
  CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")] = CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")].replace(
    bstack1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૪"),
    str(bstack1lll111_opy_)
  )
def bstack1ll11llll_opy_():
  global CONFIG
  if not bstack1l_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ૫") in CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૬")]:
    return
  bstack1l11llll1_opy_ = datetime.datetime.now()
  bstack111ll1l1_opy_ = bstack1l11llll1_opy_.strftime(bstack1l_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ૭"))
  CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")] = CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")].replace(
    bstack1l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭૰"),
    bstack111ll1l1_opy_
  )
def bstack1l1l1111l_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱") in CONFIG and not bool(CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૲")]):
    del CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૳")]
    return
  if not bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴") in CONFIG:
    CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૵")] = bstack1l_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩ૶")
  if bstack1l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭૷") in CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૸")]:
    bstack1ll11llll_opy_()
    os.environ[bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ૹ")] = CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬૺ")]
  if not bstack1l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ૻ") in CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૼ")]:
    return
  bstack1lll111_opy_ = bstack1l_opy_ (u"࠭ࠧ૽")
  bstack11ll111l1_opy_ = bstack1l11ll1ll_opy_()
  if bstack11ll111l1_opy_ != -1:
    bstack1lll111_opy_ = bstack1l_opy_ (u"ࠧࡄࡋࠣࠫ૾") + str(bstack11ll111l1_opy_)
  if bstack1lll111_opy_ == bstack1l_opy_ (u"ࠨࠩ૿"):
    bstack1l11ll11l_opy_ = bstack11ll1l1l1_opy_(CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ଀")])
    if bstack1l11ll11l_opy_ != -1:
      bstack1lll111_opy_ = str(bstack1l11ll11l_opy_)
  if bstack1lll111_opy_:
    bstack11ll11lll_opy_(bstack1lll111_opy_)
    os.environ[bstack1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧଁ")] = CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ଂ")]
def bstack1ll1llll_opy_(bstack1l11l1l11_opy_, bstack1llll11l1_opy_, path):
  bstack1l11l11ll_opy_ = {
    bstack1l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩଃ"): bstack1llll11l1_opy_
  }
  if os.path.exists(path):
    bstack11l11111_opy_ = json.load(open(path, bstack1l_opy_ (u"࠭ࡲࡣࠩ଄")))
  else:
    bstack11l11111_opy_ = {}
  bstack11l11111_opy_[bstack1l11l1l11_opy_] = bstack1l11l11ll_opy_
  with open(path, bstack1l_opy_ (u"ࠢࡸ࠭ࠥଅ")) as outfile:
    json.dump(bstack11l11111_opy_, outfile)
def bstack11ll1l1l1_opy_(bstack1l11l1l11_opy_):
  bstack1l11l1l11_opy_ = str(bstack1l11l1l11_opy_)
  bstack11111l11_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪଆ")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩଇ"))
  try:
    if not os.path.exists(bstack11111l11_opy_):
      os.makedirs(bstack11111l11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬଈ")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଉ"), bstack1l_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧଊ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l_opy_ (u"࠭ࡷࠨଋ")):
        pass
      with open(file_path, bstack1l_opy_ (u"ࠢࡸ࠭ࠥଌ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l_opy_ (u"ࠨࡴࠪ଍")) as bstack11lll11ll_opy_:
      bstack1111l1ll_opy_ = json.load(bstack11lll11ll_opy_)
    if bstack1l11l1l11_opy_ in bstack1111l1ll_opy_:
      bstack11llll1l_opy_ = bstack1111l1ll_opy_[bstack1l11l1l11_opy_][bstack1l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭଎")]
      bstack1ll1lll1l_opy_ = int(bstack11llll1l_opy_) + 1
      bstack1ll1llll_opy_(bstack1l11l1l11_opy_, bstack1ll1lll1l_opy_, file_path)
      return bstack1ll1lll1l_opy_
    else:
      bstack1ll1llll_opy_(bstack1l11l1l11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1111ll11_opy_.format(str(e)))
    return -1
def bstack11ll1ll11_opy_(config):
  if not config[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬଏ")] or not config[bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧଐ")]:
    return True
  else:
    return False
def bstack11lll11l1_opy_(config):
  if bstack1l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ଑") in config:
    del(config[bstack1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ଒")])
    return False
  if bstack11lll1ll1_opy_() < version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭ଓ")):
    return False
  if bstack11lll1ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧଔ")):
    return True
  if bstack1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩକ") in config and config[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଖ")] == False:
    return False
  else:
    return True
def bstack1ll111l1l_opy_(config, index = 0):
  global bstack1lll1ll1_opy_
  bstack111l1l1_opy_ = {}
  caps = bstack11111lll_opy_ + bstack1l1111_opy_
  if bstack1lll1ll1_opy_:
    caps += bstack1lll111ll_opy_
  for key in config:
    if key in caps + [bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ")]:
      continue
    bstack111l1l1_opy_[key] = config[key]
  if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଘ") in config:
    for bstack11l1l11_opy_ in config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଙ")][index]:
      if bstack11l1l11_opy_ in caps + [bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଚ"), bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଛ")]:
        continue
      bstack111l1l1_opy_[bstack11l1l11_opy_] = config[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ")][index][bstack11l1l11_opy_]
  bstack111l1l1_opy_[bstack1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬଝ")] = socket.gethostname()
  if bstack1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬଞ") in bstack111l1l1_opy_:
    del(bstack111l1l1_opy_[bstack1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ଟ")])
  return bstack111l1l1_opy_
def bstack111111ll_opy_(config):
  global bstack1lll1ll1_opy_
  bstack1llllll11_opy_ = {}
  caps = bstack1l1111_opy_
  if bstack1lll1ll1_opy_:
    caps+= bstack1lll111ll_opy_
  for key in caps:
    if key in config:
      bstack1llllll11_opy_[key] = config[key]
  return bstack1llllll11_opy_
def bstack1l1ll1l1l_opy_(bstack111l1l1_opy_, bstack1llllll11_opy_):
  bstack111l1l11_opy_ = {}
  for key in bstack111l1l1_opy_.keys():
    if key in bstack1l11ll1_opy_:
      bstack111l1l11_opy_[bstack1l11ll1_opy_[key]] = bstack111l1l1_opy_[key]
    else:
      bstack111l1l11_opy_[key] = bstack111l1l1_opy_[key]
  for key in bstack1llllll11_opy_:
    if key in bstack1l11ll1_opy_:
      bstack111l1l11_opy_[bstack1l11ll1_opy_[key]] = bstack1llllll11_opy_[key]
    else:
      bstack111l1l11_opy_[key] = bstack1llllll11_opy_[key]
  return bstack111l1l11_opy_
def bstack1ll1ll1_opy_(config, index = 0):
  global bstack1lll1ll1_opy_
  caps = {}
  bstack1llllll11_opy_ = bstack111111ll_opy_(config)
  bstack1ll1ll11l_opy_ = bstack1l1111_opy_
  bstack1ll1ll11l_opy_ += bstack111l111_opy_
  if bstack1lll1ll1_opy_:
    bstack1ll1ll11l_opy_ += bstack1lll111ll_opy_
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ") in config:
    if bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଡ") in config[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଢ")][index]:
      caps[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଣ")] = config[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ")][index][bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଥ")]
    if bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଦ") in config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index]:
      caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨନ")] = str(config[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪପ")])
    bstack1l111l1_opy_ = {}
    for bstack1111l1_opy_ in bstack1ll1ll11l_opy_:
      if bstack1111l1_opy_ in config[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index]:
        if bstack1111l1_opy_ == bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ବ"):
          bstack1l111l1_opy_[bstack1111l1_opy_] = str(config[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଭ")][index][bstack1111l1_opy_] * 1.0)
        else:
          bstack1l111l1_opy_[bstack1111l1_opy_] = config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩମ")][index][bstack1111l1_opy_]
        del(config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଯ")][index][bstack1111l1_opy_])
    bstack1llllll11_opy_ = update(bstack1llllll11_opy_, bstack1l111l1_opy_)
  bstack111l1l1_opy_ = bstack1ll111l1l_opy_(config, index)
  for bstack1ll1l1111_opy_ in bstack1l1111_opy_ + [bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ର"), bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ଱")]:
    if bstack1ll1l1111_opy_ in bstack111l1l1_opy_:
      bstack1llllll11_opy_[bstack1ll1l1111_opy_] = bstack111l1l1_opy_[bstack1ll1l1111_opy_]
      del(bstack111l1l1_opy_[bstack1ll1l1111_opy_])
  if bstack11lll11l1_opy_(config):
    bstack111l1l1_opy_[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଲ")] = True
    caps.update(bstack1llllll11_opy_)
    caps[bstack1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬଳ")] = bstack111l1l1_opy_
  else:
    bstack111l1l1_opy_[bstack1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଴")] = False
    caps.update(bstack1l1ll1l1l_opy_(bstack111l1l1_opy_, bstack1llllll11_opy_))
    if bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଵ") in caps:
      caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨଶ")] = caps[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଷ")]
      del(caps[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧସ")])
    if bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫହ") in caps:
      caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭଺")] = caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭଻")]
      del(caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ଼ࠧ")])
  return caps
def bstack1ll11l1ll_opy_():
  global bstack1llll1l11_opy_
  if bstack11lll1ll1_opy_() <= version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧଽ")):
    if bstack1llll1l11_opy_ != bstack1l_opy_ (u"ࠨࠩା"):
      return bstack1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥି") + bstack1llll1l11_opy_ + bstack1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢୀ")
    return bstack1ll111_opy_
  if  bstack1llll1l11_opy_ != bstack1l_opy_ (u"ࠫࠬୁ"):
    return bstack1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢୂ") + bstack1llll1l11_opy_ + bstack1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢୃ")
  return bstack11l1l_opy_
def bstack1l11ll111_opy_(options):
  return hasattr(options, bstack1l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨୄ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lllll1l_opy_(options, bstack111ll11_opy_):
  for bstack11111_opy_ in bstack111ll11_opy_:
    if bstack11111_opy_ in [bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୅"), bstack1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆")]:
      next
    if bstack11111_opy_ in options._experimental_options:
      options._experimental_options[bstack11111_opy_]= update(options._experimental_options[bstack11111_opy_], bstack111ll11_opy_[bstack11111_opy_])
    else:
      options.add_experimental_option(bstack11111_opy_, bstack111ll11_opy_[bstack11111_opy_])
  if bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨେ") in bstack111ll11_opy_:
    for arg in bstack111ll11_opy_[bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩୈ")]:
      options.add_argument(arg)
    del(bstack111ll11_opy_[bstack1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ୉")])
  if bstack1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ୊") in bstack111ll11_opy_:
    for ext in bstack111ll11_opy_[bstack1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫୋ")]:
      options.add_extension(ext)
    del(bstack111ll11_opy_[bstack1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬୌ")])
def bstack11ll111ll_opy_(options, bstack1lll11l_opy_):
  if bstack1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ୍") in bstack1lll11l_opy_:
    for bstack11l1l1111_opy_ in bstack1lll11l_opy_[bstack1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ୎")]:
      if bstack11l1l1111_opy_ in options._preferences:
        options._preferences[bstack11l1l1111_opy_] = update(options._preferences[bstack11l1l1111_opy_], bstack1lll11l_opy_[bstack1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ୏")][bstack11l1l1111_opy_])
      else:
        options.set_preference(bstack11l1l1111_opy_, bstack1lll11l_opy_[bstack1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୐")][bstack11l1l1111_opy_])
  if bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ୑") in bstack1lll11l_opy_:
    for arg in bstack1lll11l_opy_[bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      options.add_argument(arg)
def bstack1l1ll11ll_opy_(options, bstack1l1ll1111_opy_):
  if bstack1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩ୓") in bstack1l1ll1111_opy_:
    options.use_webview(bool(bstack1l1ll1111_opy_[bstack1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ୔")]))
  bstack1lllll1l_opy_(options, bstack1l1ll1111_opy_)
def bstack1l1llll_opy_(options, bstack11l1ll1l1_opy_):
  for bstack1l1lll1l1_opy_ in bstack11l1ll1l1_opy_:
    if bstack1l1lll1l1_opy_ in [bstack1l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ୕"), bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩୖ")]:
      next
    options.set_capability(bstack1l1lll1l1_opy_, bstack11l1ll1l1_opy_[bstack1l1lll1l1_opy_])
  if bstack1l_opy_ (u"ࠬࡧࡲࡨࡵࠪୗ") in bstack11l1ll1l1_opy_:
    for arg in bstack11l1ll1l1_opy_[bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ୘")]:
      options.add_argument(arg)
  if bstack1l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ୙") in bstack11l1ll1l1_opy_:
    options.use_technology_preview(bool(bstack11l1ll1l1_opy_[bstack1l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬ୚")]))
def bstack111lll_opy_(options, bstack1lll1l111_opy_):
  for bstack1lllll_opy_ in bstack1lll1l111_opy_:
    if bstack1lllll_opy_ in [bstack1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୛"), bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଡ଼")]:
      next
    options._options[bstack1lllll_opy_] = bstack1lll1l111_opy_[bstack1lllll_opy_]
  if bstack1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨଢ଼") in bstack1lll1l111_opy_:
    for bstack11lllll1l_opy_ in bstack1lll1l111_opy_[bstack1l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୞")]:
      options.add_additional_option(
          bstack11lllll1l_opy_, bstack1lll1l111_opy_[bstack1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪୟ")][bstack11lllll1l_opy_])
  if bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬୠ") in bstack1lll1l111_opy_:
    for arg in bstack1lll1l111_opy_[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ୡ")]:
      options.add_argument(arg)
def bstack11111111_opy_(options, caps):
  if not hasattr(options, bstack1l_opy_ (u"ࠩࡎࡉ࡞࠭ୢ")):
    return
  if options.KEY == bstack1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨୣ") and options.KEY in caps:
    bstack1lllll1l_opy_(options, caps[bstack1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୤")])
  elif options.KEY == bstack1l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ୥") and options.KEY in caps:
    bstack11ll111ll_opy_(options, caps[bstack1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ୦")])
  elif options.KEY == bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ୧") and options.KEY in caps:
    bstack1l1llll_opy_(options, caps[bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ୨")])
  elif options.KEY == bstack1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୩") and options.KEY in caps:
    bstack1l1ll11ll_opy_(options, caps[bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ୪")])
  elif options.KEY == bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୫") and options.KEY in caps:
    bstack111lll_opy_(options, caps[bstack1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୬")])
def bstack111l_opy_(caps):
  global bstack1lll1ll1_opy_
  if bstack1lll1ll1_opy_:
    if bstack1l11lll1l_opy_() < version.parse(bstack1l_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬ୭")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ୮")
    if bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୯") in caps:
      browser = caps[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୰")]
    elif bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫୱ") in caps:
      browser = caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ୲")]
    browser = str(browser).lower()
    if browser == bstack1l_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬ୳") or browser == bstack1l_opy_ (u"࠭ࡩࡱࡣࡧࠫ୴"):
      browser = bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ୵")
    if browser == bstack1l_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩ୶"):
      browser = bstack1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ୷")
    if browser not in [bstack1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ୸"), bstack1l_opy_ (u"ࠫࡪࡪࡧࡦࠩ୹"), bstack1l_opy_ (u"ࠬ࡯ࡥࠨ୺"), bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭୻"), bstack1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ୼")]:
      return None
    try:
      package = bstack1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ୽").format(browser)
      name = bstack1l_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪ୾")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11ll111_opy_(options):
        return None
      for bstack1ll1l1111_opy_ in caps.keys():
        options.set_capability(bstack1ll1l1111_opy_, caps[bstack1ll1l1111_opy_])
      bstack11111111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111l11_opy_(options, bstack11111ll1_opy_):
  if not bstack1l11ll111_opy_(options):
    return
  for bstack1ll1l1111_opy_ in bstack11111ll1_opy_.keys():
    if bstack1ll1l1111_opy_ in bstack111l111_opy_:
      next
    if bstack1ll1l1111_opy_ in options._caps and type(options._caps[bstack1ll1l1111_opy_]) in [dict, list]:
      options._caps[bstack1ll1l1111_opy_] = update(options._caps[bstack1ll1l1111_opy_], bstack11111ll1_opy_[bstack1ll1l1111_opy_])
    else:
      options.set_capability(bstack1ll1l1111_opy_, bstack11111ll1_opy_[bstack1ll1l1111_opy_])
  bstack11111111_opy_(options, bstack11111ll1_opy_)
  if bstack1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ୿") in options._caps:
    if options._caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ஀")] and options._caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ஁")].lower() != bstack1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧஂ"):
      del options._caps[bstack1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ஃ")]
def bstack1l1ll1l1_opy_(proxy_config):
  if bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ஄") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫஅ")] = proxy_config[bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧஆ")]
    del(proxy_config[bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨஇ")])
  if bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨஈ") in proxy_config and proxy_config[bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஉ")].lower() != bstack1l_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧஊ"):
    proxy_config[bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஋")] = bstack1l_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩ஌")
  if bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨ஍") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧஎ")] = bstack1l_opy_ (u"ࠬࡶࡡࡤࠩஏ")
  return proxy_config
def bstack11ll1111l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬஐ") in config:
    return proxy
  config[bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭஑")] = bstack1l1ll1l1_opy_(config[bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧஒ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨஓ")])
  return proxy
def bstack1lll11lll_opy_(self):
  global CONFIG
  global bstack1l11lllll_opy_
  if bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ") in CONFIG:
    return CONFIG[bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧக")]
  elif bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஖") in CONFIG:
    return CONFIG[bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ஗")]
  else:
    return bstack1l11lllll_opy_(self)
def bstack11l11l1l_opy_():
  global CONFIG
  return bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ஘") in CONFIG or bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬங") in CONFIG
def bstack1ll1lll_opy_(config):
  if not bstack11l11l1l_opy_():
    return
  if config.get(bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬச")):
    return config.get(bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭஛"))
  if config.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨஜ")):
    return config.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஝"))
def bstack11l11l_opy_():
  return bstack11l11l1l_opy_() and bstack11lll1ll1_opy_() >= version.parse(bstack1ll1111_opy_)
def bstack1l111_opy_(config):
  if bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪஞ") in config:
    return config[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫட")]
  if bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ஠") in config:
    return config[bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ஡")]
  return {}
def bstack1l1lll1l_opy_(config):
  if bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ஢") in config:
    return config[bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩண")]
  return {}
def bstack1ll1111ll_opy_(caps):
  global bstack1ll1l_opy_
  if bstack1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭த") in caps:
    caps[bstack1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ஥")][bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭஦")] = True
    if bstack1ll1l_opy_:
      caps[bstack1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ஧")][bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫந")] = bstack1ll1l_opy_
  else:
    caps[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨன")] = True
    if bstack1ll1l_opy_:
      caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬப")] = bstack1ll1l_opy_
def bstack11lll1l1_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ஫") in CONFIG and CONFIG[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ஬")]:
    bstack1ll1lll11_opy_ = bstack1l111_opy_(CONFIG)
    bstack1ll1ll1l1_opy_(CONFIG[bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ஭")], bstack1ll1lll11_opy_)
def bstack1ll1ll1l1_opy_(key, bstack1ll1lll11_opy_):
  global bstack1l1ll1ll1_opy_
  logger.info(bstack11l1l1ll_opy_)
  try:
    bstack1l1ll1ll1_opy_ = Local()
    bstack11llll1l1_opy_ = {bstack1l_opy_ (u"ࠨ࡭ࡨࡽࠬம"): key}
    bstack11llll1l1_opy_.update(bstack1ll1lll11_opy_)
    logger.debug(bstack1ll11111l_opy_.format(str(bstack11llll1l1_opy_)))
    bstack1l1ll1ll1_opy_.start(**bstack11llll1l1_opy_)
    if bstack1l1ll1ll1_opy_.isRunning():
      logger.info(bstack1l111111l_opy_)
  except Exception as e:
    bstack1l111llll_opy_(bstack1l11_opy_.format(str(e)))
def bstack1lll1lll1_opy_():
  global bstack1l1ll1ll1_opy_
  if bstack1l1ll1ll1_opy_.isRunning():
    logger.info(bstack11llllll_opy_)
    bstack1l1ll1ll1_opy_.stop()
  bstack1l1ll1ll1_opy_ = None
def bstack1l1l1ll1_opy_():
  global bstack1lllllll1_opy_
  global bstack1l1ll1_opy_
  if bstack1lllllll1_opy_:
    logger.warning(bstack1lll1ll_opy_.format(str(bstack1lllllll1_opy_)))
  logger.info(bstack1lll11l11_opy_)
  global bstack1l1ll1ll1_opy_
  if bstack1l1ll1ll1_opy_:
    bstack1lll1lll1_opy_()
  try:
    for driver in bstack1l1ll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11ll11ll1_opy_)
  bstack1l1111l1l_opy_()
def bstack1ll1l1ll1_opy_(self, *args):
  logger.error(bstack1ll11_opy_)
  bstack1l1l1ll1_opy_()
  sys.exit(1)
def bstack1l111llll_opy_(err):
  logger.critical(bstack11l1llll_opy_.format(str(err)))
  bstack1l1111l1l_opy_(bstack11l1llll_opy_.format(str(err)))
  atexit.unregister(bstack1l1l1ll1_opy_)
  sys.exit(1)
def bstack11l11ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1111l1l_opy_(message)
  atexit.unregister(bstack1l1l1ll1_opy_)
  sys.exit(1)
def bstack11ll1ll1_opy_():
  global CONFIG
  global bstack1l1l1l1_opy_
  global bstack1l1ll11l_opy_
  global bstack11lll1_opy_
  CONFIG = bstack1llll1_opy_()
  bstack11ll11l1_opy_()
  bstack11ll1l_opy_()
  CONFIG = bstack11ll1l1ll_opy_(CONFIG)
  update(CONFIG, bstack1l1ll11l_opy_)
  update(CONFIG, bstack1l1l1l1_opy_)
  CONFIG = bstack11llll1_opy_(CONFIG)
  if bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ய") in CONFIG and str(CONFIG[bstack1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧர")]).lower() == bstack1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪற"):
    bstack11lll1_opy_ = False
  if (bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨல") in CONFIG and bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩள") in bstack1l1l1l1_opy_) or (bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪழ") in CONFIG and bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫவ") not in bstack1l1ll11l_opy_):
    if os.getenv(bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ஶ")):
      CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬஷ")] = os.getenv(bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨஸ"))
    else:
      bstack1l1l1111l_opy_()
  elif (bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨஹ") not in CONFIG and bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ஺") in CONFIG) or (bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஻") in bstack1l1ll11l_opy_ and bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ஼") not in bstack1l1l1l1_opy_):
    del(CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ஽")])
  if bstack11ll1ll11_opy_(CONFIG):
    bstack1l111llll_opy_(bstack11l11ll1_opy_)
  bstack1l11l111l_opy_()
  bstack1l1ll1l11_opy_()
  if bstack1lll1ll1_opy_:
    CONFIG[bstack1l_opy_ (u"ࠪࡥࡵࡶࠧா")] = bstack1lll11_opy_(CONFIG)
    logger.info(bstack11111l1_opy_.format(CONFIG[bstack1l_opy_ (u"ࠫࡦࡶࡰࠨி")]))
def bstack1l1ll1l11_opy_():
  global CONFIG
  global bstack1lll1ll1_opy_
  if bstack1l_opy_ (u"ࠬࡧࡰࡱࠩீ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l11ll_opy_(e, bstack1l1l11ll_opy_)
    bstack1lll1ll1_opy_ = True
def bstack1lll11_opy_(config):
  bstack1l1111l_opy_ = bstack1l_opy_ (u"࠭ࠧு")
  app = config[bstack1l_opy_ (u"ࠧࡢࡲࡳࠫூ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1111l11l_opy_:
      if os.path.exists(app):
        bstack1l1111l_opy_ = bstack11ll1lll1_opy_(config, app)
      elif bstack1l1l111l_opy_(app):
        bstack1l1111l_opy_ = app
      else:
        bstack1l111llll_opy_(bstack11l111l1_opy_.format(app))
    else:
      if bstack1l1l111l_opy_(app):
        bstack1l1111l_opy_ = app
      elif os.path.exists(app):
        bstack1l1111l_opy_ = bstack11ll1lll1_opy_(app)
      else:
        bstack1l111llll_opy_(bstack1111l1l_opy_)
  else:
    if len(app) > 2:
      bstack1l111llll_opy_(bstack1llll_opy_)
    elif len(app) == 2:
      if bstack1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭௃") in app and bstack1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ௄") in app:
        if os.path.exists(app[bstack1l_opy_ (u"ࠪࡴࡦࡺࡨࠨ௅")]):
          bstack1l1111l_opy_ = bstack11ll1lll1_opy_(config, app[bstack1l_opy_ (u"ࠫࡵࡧࡴࡩࠩெ")], app[bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨே")])
        else:
          bstack1l111llll_opy_(bstack11l111l1_opy_.format(app))
      else:
        bstack1l111llll_opy_(bstack1llll_opy_)
    else:
      for key in app:
        if key in bstack1lll1l1_opy_:
          if key == bstack1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫை"):
            if os.path.exists(app[key]):
              bstack1l1111l_opy_ = bstack11ll1lll1_opy_(config, app[key])
            else:
              bstack1l111llll_opy_(bstack11l111l1_opy_.format(app))
          else:
            bstack1l1111l_opy_ = app[key]
        else:
          bstack1l111llll_opy_(bstack1llll1111_opy_)
  return bstack1l1111l_opy_
def bstack1l1l111l_opy_(bstack1l1111l_opy_):
  import re
  bstack1lll1_opy_ = re.compile(bstack1l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ௉"))
  bstack1l1l11l1_opy_ = re.compile(bstack1l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧொ"))
  if bstack1l_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨோ") in bstack1l1111l_opy_ or re.fullmatch(bstack1lll1_opy_, bstack1l1111l_opy_) or re.fullmatch(bstack1l1l11l1_opy_, bstack1l1111l_opy_):
    return True
  else:
    return False
def bstack11ll1lll1_opy_(config, path, bstack11ll1llll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l_opy_ (u"ࠪࡶࡧ࠭ௌ")).read()).hexdigest()
  bstack1lll1l1l1_opy_ = bstack1l11111l_opy_(md5_hash)
  bstack1l1111l_opy_ = None
  if bstack1lll1l1l1_opy_:
    logger.info(bstack11l1111l_opy_.format(bstack1lll1l1l1_opy_, md5_hash))
    return bstack1lll1l1l1_opy_
  bstack1l1l111_opy_ = MultipartEncoder(
    fields={
        bstack1l_opy_ (u"ࠫ࡫࡯࡬ࡦ்ࠩ"): (os.path.basename(path), open(os.path.abspath(path), bstack1l_opy_ (u"ࠬࡸࡢࠨ௎")), bstack1l_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ௏")),
        bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪௐ"): bstack11ll1llll_opy_
    }
  )
  response = requests.post(bstack11111l1l_opy_, data=bstack1l1l111_opy_,
                         headers={bstack1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ௑"): bstack1l1l111_opy_.content_type}, auth=(config[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ௒")], config[bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭௓")]))
  try:
    res = json.loads(response.text)
    bstack1l1111l_opy_ = res[bstack1l_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ௔")]
    logger.info(bstack11ll1l1_opy_.format(bstack1l1111l_opy_))
    bstack1ll1lll1_opy_(md5_hash, bstack1l1111l_opy_)
  except ValueError as err:
    bstack1l111llll_opy_(bstack1ll11ll11_opy_.format(str(err)))
  return bstack1l1111l_opy_
def bstack1l11l111l_opy_():
  global CONFIG
  global bstack1l111ll1l_opy_
  bstack1ll111111_opy_ = 0
  bstack1l1l1l1l1_opy_ = 1
  if bstack1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ௕") in CONFIG:
    bstack1l1l1l1l1_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭௖")]
  if bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪௗ") in CONFIG:
    bstack1ll111111_opy_ = len(CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௘")])
  bstack1l111ll1l_opy_ = int(bstack1l1l1l1l1_opy_) * int(bstack1ll111111_opy_)
def bstack1l11111l_opy_(md5_hash):
  bstack11lll1l11_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠩࢁࠫ௙")), bstack1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ௚"), bstack1l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ௛"))
  if os.path.exists(bstack11lll1l11_opy_):
    bstack1l1111ll1_opy_ = json.load(open(bstack11lll1l11_opy_,bstack1l_opy_ (u"ࠬࡸࡢࠨ௜")))
    if md5_hash in bstack1l1111ll1_opy_:
      bstack11l1ll1ll_opy_ = bstack1l1111ll1_opy_[md5_hash]
      bstack1llllll1l_opy_ = datetime.datetime.now()
      bstack1l1lll_opy_ = datetime.datetime.strptime(bstack11l1ll1ll_opy_[bstack1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ௝")], bstack1l_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫ௞"))
      if (bstack1llllll1l_opy_ - bstack1l1lll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11l1ll1ll_opy_[bstack1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭௟")]):
        return None
      return bstack11l1ll1ll_opy_[bstack1l_opy_ (u"ࠩ࡬ࡨࠬ௠")]
  else:
    return None
def bstack1ll1lll1_opy_(md5_hash, bstack1l1111l_opy_):
  bstack11111l11_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬ௡")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ௢"))
  if not os.path.exists(bstack11111l11_opy_):
    os.makedirs(bstack11111l11_opy_)
  bstack11lll1l11_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠬࢄࠧ௣")), bstack1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭௤"), bstack1l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ௥"))
  bstack1111ll1_opy_ = {
    bstack1l_opy_ (u"ࠨ࡫ࡧࠫ௦"): bstack1l1111l_opy_,
    bstack1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ௧"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ௨")),
    bstack1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ௩"): str(__version__)
  }
  if os.path.exists(bstack11lll1l11_opy_):
    bstack1l1111ll1_opy_ = json.load(open(bstack11lll1l11_opy_,bstack1l_opy_ (u"ࠬࡸࡢࠨ௪")))
  else:
    bstack1l1111ll1_opy_ = {}
  bstack1l1111ll1_opy_[md5_hash] = bstack1111ll1_opy_
  with open(bstack11lll1l11_opy_, bstack1l_opy_ (u"ࠨࡷࠬࠤ௫")) as outfile:
    json.dump(bstack1l1111ll1_opy_, outfile)
def bstack111ll11l_opy_(self):
  return
def bstack1l111lll1_opy_(self):
  return
def bstack1l11l1lll_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1111l11_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l1l11lll_opy_
  global bstack1l1l1lll1_opy_
  global bstack1l1llll1_opy_
  global bstack1l11l111_opy_
  global bstack1llllllll_opy_
  global bstack1l111l_opy_
  global bstack1l1ll1_opy_
  global bstack1l111l111_opy_
  CONFIG[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ௬")] = str(bstack1llllllll_opy_) + str(__version__)
  command_executor = bstack1ll11l1ll_opy_()
  logger.debug(bstack1ll11111_opy_.format(command_executor))
  proxy = bstack11ll1111l_opy_(CONFIG, proxy)
  bstack111111l1_opy_ = 0 if bstack1l1l1lll1_opy_ < 0 else bstack1l1l1lll1_opy_
  if bstack1l11l111_opy_ is True:
    bstack111111l1_opy_ = int(threading.current_thread().getName())
  bstack11111ll1_opy_ = bstack1ll1ll1_opy_(CONFIG, bstack111111l1_opy_)
  logger.debug(bstack1llll1l1_opy_.format(str(bstack11111ll1_opy_)))
  if bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ௭") in CONFIG and CONFIG[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭௮")]:
    bstack1ll1111ll_opy_(bstack11111ll1_opy_)
  if desired_capabilities:
    bstack1l11l1_opy_ = bstack11ll1l1ll_opy_(desired_capabilities)
    bstack1l11l1_opy_[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ௯")] = bstack11lll11l1_opy_(CONFIG)
    bstack1lllll1ll_opy_ = bstack1ll1ll1_opy_(bstack1l11l1_opy_)
    if bstack1lllll1ll_opy_:
      bstack11111ll1_opy_ = update(bstack1lllll1ll_opy_, bstack11111ll1_opy_)
    desired_capabilities = None
  if options:
    bstack111l11_opy_(options, bstack11111ll1_opy_)
  if not options:
    options = bstack111l_opy_(bstack11111ll1_opy_)
  if proxy and bstack11lll1ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ௰")):
    options.proxy(proxy)
  if options and bstack11lll1ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ௱")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack11lll1ll1_opy_() < version.parse(bstack1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ௲")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11111ll1_opy_)
  logger.info(bstack1l1ll111l_opy_)
  if bstack11lll1ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ௳")):
    bstack1l111l_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11lll1ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ௴")):
    bstack1l111l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11lll1ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ௵")):
    bstack1l111l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l111l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack1lll11ll1_opy_ = bstack1l_opy_ (u"ࠪࠫ௶")
    if bstack11lll1ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ௷")):
      bstack1lll11ll1_opy_ = self.caps.get(bstack1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ௸"))
    else:
      bstack1lll11ll1_opy_ = self.capabilities.get(bstack1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ௹"))
    if bstack1lll11ll1_opy_:
      if bstack11lll1ll1_opy_() <= version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ௺")):
        self.command_executor._url = bstack1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ௻") + bstack1llll1l11_opy_ + bstack1l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ௼")
      else:
        self.command_executor._url = bstack1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ௽") + bstack1lll11ll1_opy_ + bstack1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ௾")
      logger.debug(bstack1l111l11_opy_.format(bstack1lll11ll1_opy_))
    else:
      logger.debug(bstack1ll111l_opy_.format(bstack1l_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ௿")))
  except Exception as e:
    logger.debug(bstack1ll111l_opy_.format(e))
  bstack111l11l1_opy_(bstack1l1l1lll1_opy_, bstack1l111l111_opy_)
  bstack1l1l11lll_opy_ = self.session_id
  bstack1l1ll1_opy_.append(self)
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఀ") in CONFIG and bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఁ") in CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫం")][bstack111111l1_opy_]:
    bstack1l1llll1_opy_ = CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬః")][bstack111111l1_opy_][bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨఄ")]
  logger.debug(bstack111111_opy_.format(bstack1l1l11lll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack11l1l111l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l11111_opy_
      if(bstack1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺ࠱࡮ࡸࠨఅ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠬࢄࠧఆ")), bstack1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ఇ"), bstack1l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩఈ")), bstack1l_opy_ (u"ࠨࡹࠪఉ")) as fp:
          fp.write(bstack1l_opy_ (u"ࠤࠥఊ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧఋ")))):
          with open(args[1], bstack1l_opy_ (u"ࠫࡷ࠭ఌ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l_opy_ (u"ࠬࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦ࡟࡯ࡧࡺࡔࡦ࡭ࡥࠩࡥࡲࡲࡹ࡫ࡸࡵ࠮ࠣࡴࡦ࡭ࡥࠡ࠿ࠣࡺࡴ࡯ࡤࠡ࠲ࠬࠫ఍") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l11l_opy_)
            lines.insert(1, bstack111ll1ll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣఎ")), bstack1l_opy_ (u"ࠧࡸࠩఏ")) as bstack11l1ll_opy_:
              bstack11l1ll_opy_.writelines(lines)
        CONFIG[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪఐ")] = str(bstack1llllllll_opy_) + str(__version__)
        bstack111111l1_opy_ = 0 if bstack1l1l1lll1_opy_ < 0 else bstack1l1l1lll1_opy_
        if bstack1l11l111_opy_ is True:
          bstack111111l1_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ఑")] = False
        CONFIG[bstack1l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤఒ")] = True
        bstack11111ll1_opy_ = bstack1ll1ll1_opy_(CONFIG, bstack111111l1_opy_)
        logger.debug(bstack1llll1l1_opy_.format(str(bstack11111ll1_opy_)))
        if CONFIG[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨఓ")]:
          bstack1ll1111ll_opy_(bstack11111ll1_opy_)
        if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఔ") in CONFIG and bstack1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫక") in CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఖ")][bstack111111l1_opy_]:
          bstack1l1llll1_opy_ = CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫగ")][bstack111111l1_opy_][bstack1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧఘ")]
        args.append(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬఙ")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫచ"), bstack1l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧఛ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11111ll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣజ"))
      bstack1l11111_opy_ = True
      return bstack1l1l11ll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l1l11lll_opy_
    global bstack1l1l1lll1_opy_
    global bstack1l1llll1_opy_
    global bstack1l11l111_opy_
    global bstack1llllllll_opy_
    global bstack1l111l_opy_
    CONFIG[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩఝ")] = str(bstack1llllllll_opy_) + str(__version__)
    bstack111111l1_opy_ = 0 if bstack1l1l1lll1_opy_ < 0 else bstack1l1l1lll1_opy_
    if bstack1l11l111_opy_ is True:
      bstack111111l1_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢఞ")] = True
    bstack11111ll1_opy_ = bstack1ll1ll1_opy_(CONFIG, bstack111111l1_opy_)
    logger.debug(bstack1llll1l1_opy_.format(str(bstack11111ll1_opy_)))
    if CONFIG[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ట")]:
      bstack1ll1111ll_opy_(bstack11111ll1_opy_)
    if bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఠ") in CONFIG and bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩడ") in CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఢ")][bstack111111l1_opy_]:
      bstack1l1llll1_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩణ")][bstack111111l1_opy_][bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬత")]
    import urllib
    import json
    bstack1ll11l11l_opy_ = bstack1l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪథ") + urllib.parse.quote(json.dumps(bstack11111ll1_opy_))
    browser = self.connect(bstack1ll11l11l_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1l111ll_opy_():
    global bstack1l11111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l1_opy_
        bstack1l11111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l1l111l_opy_
      bstack1l11111_opy_ = True
    except Exception as e:
      pass
def bstack1lll11ll_opy_(context, bstack1lll1lll_opy_):
  try:
    context.page.evaluate(bstack1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥద"), bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧధ")+ json.dumps(bstack1lll1lll_opy_) + bstack1l_opy_ (u"ࠦࢂࢃࠢన"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥ఩"), e)
def bstack11l1111_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢప"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬఫ") + json.dumps(message) + bstack1l_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫబ") + json.dumps(level) + bstack1l_opy_ (u"ࠩࢀࢁࠬభ"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨమ"), e)
def bstack11l1lllll_opy_(context, status, message = bstack1l_opy_ (u"ࠦࠧయ")):
  try:
    if(status == bstack1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧర")):
      context.page.evaluate(bstack1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢఱ"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠨల") + json.dumps(bstack1l_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢࠥళ") + str(message)) + bstack1l_opy_ (u"ࠩ࠯ࠦࡸࡺࡡࡵࡷࡶࠦ࠿࠭ఴ") + json.dumps(status) + bstack1l_opy_ (u"ࠥࢁࢂࠨవ"))
    else:
      context.page.evaluate(bstack1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧశ"), bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿࠭ష") + json.dumps(status) + bstack1l_opy_ (u"ࠨࡽࡾࠤస"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦహ"), e)
def bstack1l1l1l11_opy_(self, url):
  global bstack1ll11l1l1_opy_
  try:
    bstack1l1l111l1_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1l1llll_opy_.format(str(err)))
  try:
    bstack1ll11l1l1_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1ll11_opy_ = str(e)
      if any(err_msg in bstack1ll1ll11_opy_ for err_msg in bstack1l111111_opy_):
        bstack1l1l111l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1l1llll_opy_.format(str(err)))
    raise e
def bstack11l1l111_opy_(self):
  global bstack111l1l_opy_
  bstack111l1l_opy_ = self
  return
def bstack1l111l1l1_opy_(self, test):
  global CONFIG
  global bstack111l1l_opy_
  global bstack1l1l11lll_opy_
  global bstack11l1l11l1_opy_
  global bstack1l1llll1_opy_
  global bstack1l1l1ll_opy_
  global bstack1ll11l11_opy_
  global bstack1l1ll1_opy_
  try:
    if not bstack1l1l11lll_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪ఺")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ఻"), bstack1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸ఼ࠬ"))) as f:
        bstack1111lll_opy_ = json.loads(bstack1l_opy_ (u"ࠦࢀࠨఽ") + f.read().strip() + bstack1l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧా") + bstack1l_opy_ (u"ࠨࡽࠣి"))
        bstack1l1l11lll_opy_ = bstack1111lll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l1ll1_opy_:
    for driver in bstack1l1ll1_opy_:
      if bstack1l1l11lll_opy_ == driver.session_id:
        if test:
          bstack1l1llll1l_opy_ = str(test.data)
        if not bstack1111l11_opy_ and bstack1l1llll1l_opy_:
          bstack1l1111111_opy_ = {
            bstack1l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧీ"): bstack1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩు"),
            bstack1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬూ"): {
              bstack1l_opy_ (u"ࠪࡲࡦࡳࡥࠨృ"): bstack1l1llll1l_opy_
            }
          }
          bstack111l1_opy_ = bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩౄ").format(json.dumps(bstack1l1111111_opy_))
          driver.execute_script(bstack111l1_opy_)
        if bstack11l1l11l1_opy_:
          bstack11ll1ll_opy_ = {
            bstack1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ౅"): bstack1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨె"),
            bstack1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪే"): {
              bstack1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ై"): bstack1l1llll1l_opy_ + bstack1l_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ౉"),
              bstack1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩొ"): bstack1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩో")
            }
          }
          bstack1l1111111_opy_ = {
            bstack1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬౌ"): bstack1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴ్ࠩ"),
            bstack1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ౎"): {
              bstack1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ౏"): bstack1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౐")
            }
          }
          if bstack11l1l11l1_opy_.status == bstack1l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ౑"):
            bstack1l1lllll_opy_ = bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ౒").format(json.dumps(bstack11ll1ll_opy_))
            driver.execute_script(bstack1l1lllll_opy_)
            bstack111l1_opy_ = bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ౓").format(json.dumps(bstack1l1111111_opy_))
            driver.execute_script(bstack111l1_opy_)
          elif bstack11l1l11l1_opy_.status == bstack1l_opy_ (u"࠭ࡆࡂࡋࡏࠫ౔"):
            reason = bstack1l_opy_ (u"ౕࠢࠣ")
            bstack11l11l11_opy_ = bstack1l1llll1l_opy_ + bstack1l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥౖࠩ")
            if bstack11l1l11l1_opy_.message:
              reason = str(bstack11l1l11l1_opy_.message)
              bstack11l11l11_opy_ = bstack11l11l11_opy_ + bstack1l_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩ౗") + reason
            bstack11ll1ll_opy_[bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ౘ")] = {
              bstack1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪౙ"): bstack1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫౚ"),
              bstack1l_opy_ (u"࠭ࡤࡢࡶࡤࠫ౛"): bstack11l11l11_opy_
            }
            bstack1l1111111_opy_[bstack1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ౜")] = {
              bstack1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨౝ"): bstack1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౞"),
              bstack1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ౟"): reason
            }
            bstack1l1lllll_opy_ = bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩౠ").format(json.dumps(bstack11ll1ll_opy_))
            driver.execute_script(bstack1l1lllll_opy_)
            bstack111l1_opy_ = bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪౡ").format(json.dumps(bstack1l1111111_opy_))
            driver.execute_script(bstack111l1_opy_)
  elif bstack1l1l11lll_opy_:
    try:
      data = {}
      bstack1l1llll1l_opy_ = None
      if test:
        bstack1l1llll1l_opy_ = str(test.data)
      if not bstack1111l11_opy_ and bstack1l1llll1l_opy_:
        data[bstack1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫౢ")] = bstack1l1llll1l_opy_
      if bstack11l1l11l1_opy_:
        if bstack11l1l11l1_opy_.status == bstack1l_opy_ (u"ࠧࡑࡃࡖࡗࠬౣ"):
          data[bstack1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ౤")] = bstack1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౥")
        elif bstack11l1l11l1_opy_.status == bstack1l_opy_ (u"ࠪࡊࡆࡏࡌࠨ౦"):
          data[bstack1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ౧")] = bstack1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ౨")
          if bstack11l1l11l1_opy_.message:
            data[bstack1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭౩")] = str(bstack11l1l11l1_opy_.message)
      user = CONFIG[bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ౪")]
      key = CONFIG[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ౫")]
      url = bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧ౬").format(user, key, bstack1l1l11lll_opy_)
      headers = {
        bstack1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ౭"): bstack1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ౮"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack111ll1_opy_.format(str(e)))
  if bstack111l1l_opy_:
    bstack1ll11l11_opy_(bstack111l1l_opy_)
  bstack1l1l1ll_opy_(self, test)
def bstack11ll1l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll111l_opy_
  bstack1llll111l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1l11l1_opy_
  bstack11l1l11l1_opy_ = self._test
def bstack11l1llll1_opy_():
  global bstack1lllll11_opy_
  try:
    if os.path.exists(bstack1lllll11_opy_):
      os.remove(bstack1lllll11_opy_)
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ౯") + str(e))
def bstack1ll1l11_opy_():
  global bstack1lllll11_opy_
  bstack11l11111_opy_ = {}
  try:
    if not os.path.isfile(bstack1lllll11_opy_):
      with open(bstack1lllll11_opy_, bstack1l_opy_ (u"࠭ࡷࠨ౰")):
        pass
      with open(bstack1lllll11_opy_, bstack1l_opy_ (u"ࠢࡸ࠭ࠥ౱")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1lllll11_opy_):
      bstack11l11111_opy_ = json.load(open(bstack1lllll11_opy_, bstack1l_opy_ (u"ࠨࡴࡥࠫ౲")))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ౳") + str(e))
  finally:
    return bstack11l11111_opy_
def bstack111l11l1_opy_(platform_index, item_index):
  global bstack1lllll11_opy_
  try:
    bstack11l11111_opy_ = bstack1ll1l11_opy_()
    bstack11l11111_opy_[item_index] = platform_index
    with open(bstack1lllll11_opy_, bstack1l_opy_ (u"ࠥࡻ࠰ࠨ౴")) as outfile:
      json.dump(bstack11l11111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ౵") + str(e))
def bstack1ll1111l_opy_(bstack11lll11l_opy_):
  global CONFIG
  bstack1lll1l1l_opy_ = bstack1l_opy_ (u"ࠬ࠭౶")
  if not bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౷") in CONFIG:
    logger.info(bstack1l_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫ౸"))
  try:
    platform = CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౹")][bstack11lll11l_opy_]
    if bstack1l_opy_ (u"ࠩࡲࡷࠬ౺") in platform:
      bstack1lll1l1l_opy_ += str(platform[bstack1l_opy_ (u"ࠪࡳࡸ࠭౻")]) + bstack1l_opy_ (u"ࠫ࠱ࠦࠧ౼")
    if bstack1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ౽") in platform:
      bstack1lll1l1l_opy_ += str(platform[bstack1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ౾")]) + bstack1l_opy_ (u"ࠧ࠭ࠢࠪ౿")
    if bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬಀ") in platform:
      bstack1lll1l1l_opy_ += str(platform[bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ಁ")]) + bstack1l_opy_ (u"ࠪ࠰ࠥ࠭ಂ")
    if bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ಃ") in platform:
      bstack1lll1l1l_opy_ += str(platform[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ಄")]) + bstack1l_opy_ (u"࠭ࠬࠡࠩಅ")
    if bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬಆ") in platform:
      bstack1lll1l1l_opy_ += str(platform[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ಇ")]) + bstack1l_opy_ (u"ࠩ࠯ࠤࠬಈ")
    if bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫಉ") in platform:
      bstack1lll1l1l_opy_ += str(platform[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬಊ")]) + bstack1l_opy_ (u"ࠬ࠲ࠠࠨಋ")
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭ಌ") + str(e))
  finally:
    if bstack1lll1l1l_opy_[len(bstack1lll1l1l_opy_) - 2:] == bstack1l_opy_ (u"ࠧ࠭ࠢࠪ಍"):
      bstack1lll1l1l_opy_ = bstack1lll1l1l_opy_[:-2]
    return bstack1lll1l1l_opy_
def bstack1lll1ll11_opy_(path, bstack1lll1l1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1llllll_opy_ = ET.parse(path)
    bstack1lll1l1ll_opy_ = bstack1llllll_opy_.getroot()
    bstack111l111l_opy_ = None
    for suite in bstack1lll1l1ll_opy_.iter(bstack1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧಎ")):
      if bstack1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩಏ") in suite.attrib:
        suite.attrib[bstack1l_opy_ (u"ࠪࡲࡦࡳࡥࠨಐ")] += bstack1l_opy_ (u"ࠫࠥ࠭಑") + bstack1lll1l1l_opy_
        bstack111l111l_opy_ = suite
    bstack1l11ll1l1_opy_ = None
    for robot in bstack1lll1l1ll_opy_.iter(bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫಒ")):
      bstack1l11ll1l1_opy_ = robot
    bstack1l11l11_opy_ = len(bstack1l11ll1l1_opy_.findall(bstack1l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬಓ")))
    if bstack1l11l11_opy_ == 1:
      bstack1l11ll1l1_opy_.remove(bstack1l11ll1l1_opy_.findall(bstack1l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ಔ"))[0])
      bstack1l1l11_opy_ = ET.Element(bstack1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧಕ"), attrib={bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧಖ"):bstack1l_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪಗ"), bstack1l_opy_ (u"ࠫ࡮ࡪࠧಘ"):bstack1l_opy_ (u"ࠬࡹ࠰ࠨಙ")})
      bstack1l11ll1l1_opy_.insert(1, bstack1l1l11_opy_)
      bstack1l1lll111_opy_ = None
      for suite in bstack1l11ll1l1_opy_.iter(bstack1l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬಚ")):
        bstack1l1lll111_opy_ = suite
      bstack1l1lll111_opy_.append(bstack111l111l_opy_)
      bstack1l11l1111_opy_ = None
      for status in bstack111l111l_opy_.iter(bstack1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧಛ")):
        bstack1l11l1111_opy_ = status
      bstack1l1lll111_opy_.append(bstack1l11l1111_opy_)
    bstack1llllll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭ಜ") + str(e))
def bstack111ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l11l1ll1_opy_
  global CONFIG
  if bstack1l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨಝ") in options:
    del options[bstack1l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢಞ")]
  bstack1l11l11ll_opy_ = bstack1ll1l11_opy_()
  for bstack11l11lll_opy_ in bstack1l11l11ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫಟ"), str(bstack11l11lll_opy_), bstack1l_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩಠ"))
    bstack1lll1ll11_opy_(path, bstack1ll1111l_opy_(bstack1l11l11ll_opy_[bstack11l11lll_opy_]))
  bstack11l1llll1_opy_()
  return bstack1l11l1ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll1l11ll_opy_(self, ff_profile_dir):
  global bstack11lllll1_opy_
  if not ff_profile_dir:
    return None
  return bstack11lllll1_opy_(self, ff_profile_dir)
def bstack1111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll1l_opy_
  bstack11llll_opy_ = []
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಡ") in CONFIG:
    bstack11llll_opy_ = CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಢ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤಣ")],
      pabot_args[bstack1l_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥತ")],
      argfile,
      pabot_args.get(bstack1l_opy_ (u"ࠥ࡬࡮ࡼࡥࠣಥ")),
      pabot_args[bstack1l_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢದ")],
      platform[0],
      bstack1ll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧಧ")] or [(bstack1l_opy_ (u"ࠨࠢನ"), None)]
    for platform in enumerate(bstack11llll_opy_)
  ]
def bstack1ll1l1l11_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1lll111l1_opy_=bstack1l_opy_ (u"ࠧࠨ಩")):
  global bstack11llll11l_opy_
  self.platform_index = platform_index
  self.bstack11l1lll1_opy_ = bstack1lll111l1_opy_
  bstack11llll11l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll11ll1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111ll1l_opy_
  global bstack1l11ll_opy_
  if not bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಪ") in item.options:
    item.options[bstack1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫಫ")] = []
  for v in item.options[bstack1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಬ")]:
    if bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪಭ") in v:
      item.options[bstack1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧಮ")].remove(v)
    if bstack1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ಯ") in v:
      item.options[bstack1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩರ")].remove(v)
  item.options[bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಱ")].insert(0, bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫಲ").format(item.platform_index))
  item.options[bstack1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಳ")].insert(0, bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ಴").format(item.bstack11l1lll1_opy_))
  if bstack1l11ll_opy_:
    item.options[bstack1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧವ")].insert(0, bstack1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩಶ").format(bstack1l11ll_opy_))
  return bstack111ll1l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1lll11l1_opy_(command, item_index):
  global bstack1l11ll_opy_
  if bstack1l11ll_opy_:
    command[0] = command[0].replace(bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಷ"), bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬಸ") + str(item_index) + bstack1l11ll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಹ"), bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧ಺") + str(item_index), 1)
def bstack1llll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11lll1l1l_opy_
  bstack1lll11l1_opy_(command, item_index)
  return bstack11lll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11llll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11lll1l1l_opy_
  bstack1lll11l1_opy_(command, item_index)
  return bstack11lll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1ll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11lll1l1l_opy_
  bstack1lll11l1_opy_(command, item_index)
  return bstack11lll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1l11l11l_opy_(self, runner, quiet=False, capture=True):
  global bstack11ll11l_opy_
  bstack1ll1l11l1_opy_ = bstack11ll11l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫ಻")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳ಼ࠩ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1l11l1_opy_
def bstack111111l_opy_(self, name, context, *args):
  global bstack11111ll_opy_
  if name in [bstack1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧಽ"), bstack1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩಾ")]:
    bstack11111ll_opy_(self, name, context, *args)
  if name == bstack1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩಿ"):
    try:
      if(not bstack1111l11_opy_):
        bstack1lll1lll_opy_ = str(self.feature.name)
        bstack1lll11ll_opy_(context, bstack1lll1lll_opy_)
        context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧೀ") + json.dumps(bstack1lll1lll_opy_) + bstack1l_opy_ (u"ࠪࢁࢂ࠭ು"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫೂ").format(str(e)))
  if name == bstack1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧೃ"):
    try:
      if not hasattr(self, bstack1l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨೄ")):
        self.driver_before_scenario = True
      if(not bstack1111l11_opy_):
        bstack11l1l1l1_opy_ = args[0].name
        bstack111l1lll_opy_ = bstack1lll1lll_opy_ = str(self.feature.name)
        bstack1lll1lll_opy_ = bstack111l1lll_opy_ + bstack1l_opy_ (u"ࠧࠡ࠯ࠣࠫ೅") + bstack11l1l1l1_opy_
        if self.driver_before_scenario:
          bstack1lll11ll_opy_(context, bstack1lll1lll_opy_)
          context.browser.execute_script(bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ೆ") + json.dumps(bstack1lll1lll_opy_) + bstack1l_opy_ (u"ࠩࢀࢁࠬೇ"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫೈ").format(str(e)))
  if name == bstack1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ೉"):
    try:
      bstack1lll1ll1l_opy_ = args[0].status.name
      if str(bstack1lll1ll1l_opy_).lower() == bstack1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬೊ"):
        bstack1111111l_opy_ = bstack1l_opy_ (u"࠭ࠧೋ")
        bstack1l111ll1_opy_ = bstack1l_opy_ (u"ࠧࠨೌ")
        bstack1ll1llll1_opy_ = bstack1l_opy_ (u"ࠨ್ࠩ")
        try:
          import traceback
          bstack1111111l_opy_ = self.exception.__class__.__name__
          bstack1ll11ll1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l111ll1_opy_ = bstack1l_opy_ (u"ࠩࠣࠫ೎").join(bstack1ll11ll1_opy_)
          bstack1ll1llll1_opy_ = bstack1ll11ll1_opy_[-1]
        except Exception as e:
          logger.debug(bstack11lll11_opy_.format(str(e)))
        bstack1111111l_opy_ += bstack1ll1llll1_opy_
        bstack11l1111_opy_(context, json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ೏") + str(bstack1l111ll1_opy_)), bstack1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ೐"))
        if self.driver_before_scenario:
          bstack11l1lllll_opy_(context, bstack1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ೑"), bstack1111111l_opy_)
        context.browser.execute_script(bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ೒") + json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ೓") + str(bstack1l111ll1_opy_)) + bstack1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ೔"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩೕ") + json.dumps(bstack1l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢೖ") + str(bstack1111111l_opy_)) + bstack1l_opy_ (u"ࠫࢂࢃࠧ೗"))
      else:
        bstack11l1111_opy_(context, bstack1l_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ೘"), bstack1l_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ೙"))
        if self.driver_before_scenario:
          bstack11l1lllll_opy_(context, bstack1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ೚"))
        context.browser.execute_script(bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭೛") + json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ೜")) + bstack1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩೝ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨೞ"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ೟").format(str(e)))
  if name == bstack1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ೠ"):
    try:
      if context.failed is True:
        bstack111l1l1l_opy_ = []
        bstack111lll11_opy_ = []
        bstack11lll1lll_opy_ = []
        bstack11lll1l_opy_ = bstack1l_opy_ (u"ࠧࠨೡ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack111l1l1l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll11ll1_opy_ = traceback.format_tb(exc_tb)
            bstack1111ll_opy_ = bstack1l_opy_ (u"ࠨࠢࠪೢ").join(bstack1ll11ll1_opy_)
            bstack111lll11_opy_.append(bstack1111ll_opy_)
            bstack11lll1lll_opy_.append(bstack1ll11ll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack11lll11_opy_.format(str(e)))
        bstack1111111l_opy_ = bstack1l_opy_ (u"ࠩࠪೣ")
        for i in range(len(bstack111l1l1l_opy_)):
          bstack1111111l_opy_ += bstack111l1l1l_opy_[i] + bstack11lll1lll_opy_[i] + bstack1l_opy_ (u"ࠪࡠࡳ࠭೤")
        bstack11lll1l_opy_ = bstack1l_opy_ (u"ࠫࠥ࠭೥").join(bstack111lll11_opy_)
        if not self.driver_before_scenario:
          bstack11l1111_opy_(context, bstack11lll1l_opy_, bstack1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ೦"))
          bstack11l1lllll_opy_(context, bstack1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ೧"), bstack1111111l_opy_)
          context.browser.execute_script(bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ೨") + json.dumps(bstack11lll1l_opy_) + bstack1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ೩"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ೪") + json.dumps(bstack1l_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ೫") + str(bstack1111111l_opy_)) + bstack1l_opy_ (u"ࠫࢂࢃࠧ೬"))
      else:
        if not self.driver_before_scenario:
          bstack11l1111_opy_(context, bstack1l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ೭") + str(self.feature.name) + bstack1l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ೮"), bstack1l_opy_ (u"ࠢࡪࡰࡩࡳࠧ೯"))
          bstack11l1lllll_opy_(context, bstack1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ೰"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧೱ") + json.dumps(bstack1l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨೲ") + str(self.feature.name) + bstack1l_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨೳ")) + bstack1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ೴"))
          context.browser.execute_script(bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪ೵"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ೶").format(str(e)))
  if name in [bstack1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ೷"), bstack1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ೸")]:
    bstack11111ll_opy_(self, name, context, *args)
    if (name == bstack1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೹") and self.driver_before_scenario) or (name == bstack1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫ೺") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack1lll11l1l_opy_(config, startdir):
  return bstack1l_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥ೻").format(bstack1l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ೼"))
class Notset:
  def __repr__(self):
    return bstack1l_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤ೽")
notset = Notset()
def bstack1ll1ll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1l1ll1l_opy_
  if str(name).lower() == bstack1l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ೾"):
    return bstack1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ೿")
  else:
    return bstack1l1l1ll1l_opy_(self, name, default, skip)
def bstack1l1l1ll11_opy_(item, when):
  global bstack11l11_opy_
  try:
    bstack11l11_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11l1l1_opy_():
  return
def bstack1111l1l1_opy_(bstack1ll11lll_opy_):
  global bstack1llllllll_opy_
  global bstack1l11111_opy_
  bstack1llllllll_opy_ = bstack1ll11lll_opy_
  logger.info(bstack1lll111l_opy_.format(bstack1llllllll_opy_.split(bstack1l_opy_ (u"ࠪ࠱ࠬഀ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack111ll11l_opy_
    Service.stop = bstack1l111lll1_opy_
    webdriver.Remote.__init__ = bstack1l1111l11_opy_
    webdriver.Remote.get = bstack1l1l1l11_opy_
    WebDriver.close = bstack1l11l1lll_opy_
    bstack1l11111_opy_ = True
  except Exception as e:
    pass
  bstack1l1l111ll_opy_()
  if not bstack1l11111_opy_:
    bstack11l11ll_opy_(bstack1l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨഁ"), bstack1l1ll1ll_opy_)
  if bstack11l11l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1lll11lll_opy_
    except Exception as e:
      logger.error(bstack1ll111l1_opy_.format(str(e)))
  if (bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫം") in str(bstack1ll11lll_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll1l11ll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11l1l111_opy_
      except Exception as e:
        logger.warn(bstack1l1ll11l1_opy_ + str(e))
    except Exception as e:
      bstack11l11ll_opy_(e, bstack1l1ll11l1_opy_)
    Output.end_test = bstack1l111l1l1_opy_
    TestStatus.__init__ = bstack11ll1l11_opy_
    QueueItem.__init__ = bstack1ll1l1l11_opy_
    pabot._create_items = bstack1111_opy_
    try:
      from pabot import __version__ as bstack11l1l11l_opy_
      if version.parse(bstack11l1l11l_opy_) >= version.parse(bstack1l_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭ഃ")):
        pabot._run = bstack1ll1l1l_opy_
      elif version.parse(bstack11l1l11l_opy_) >= version.parse(bstack1l_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧഄ")):
        pabot._run = bstack11llll1ll_opy_
      else:
        pabot._run = bstack1llll1l1l_opy_
    except Exception as e:
      pabot._run = bstack1llll1l1l_opy_
    pabot._create_command_for_execution = bstack1ll11ll1l_opy_
    pabot._report_results = bstack111ll_opy_
  if bstack1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨഅ") in str(bstack1ll11lll_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l11ll_opy_(e, bstack1ll111l11_opy_)
    Runner.run_hook = bstack111111l_opy_
    Step.run = bstack1l11l11l_opy_
  if bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩആ") in str(bstack1ll11lll_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack1lll11l1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11l1l1_opy_
      Config.getoption = bstack1ll1ll_opy_
      runner._update_current_test_var = bstack1l1l1ll11_opy_
    except Exception as e:
      pass
def bstack1ll1l11l_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪഇ") in CONFIG and int(CONFIG[bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫഈ")]) > 1:
    logger.warn(bstack1lll1l11l_opy_)
def bstack11lllll11_opy_(bstack1l1l1lll_opy_, index):
  bstack1111l1l1_opy_(bstack1lllll111_opy_)
  exec(open(bstack1l1l1lll_opy_).read())
def bstack1l1l1l1l_opy_(arg):
  arg.append(bstack1l_opy_ (u"ࠧ࠳࠭ࡤࡣࡳࡸࡺࡸࡥ࠾ࡵࡼࡷࠧഉ"))
  arg.append(bstack1l_opy_ (u"ࠨ࠭ࡘࠤഊ"))
  arg.append(bstack1l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥഋ"))
  global CONFIG
  bstack1111l1l1_opy_(bstack1111111_opy_)
  os.environ[bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩഌ")] = CONFIG[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ഍")]
  os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭എ")] = CONFIG[bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഏ")]
  from _pytest.config import main as bstack11ll_opy_
  bstack11ll_opy_(arg)
def bstack111lllll_opy_(arg):
  bstack1111l1l1_opy_(bstack1llll11_opy_)
  from behave.__main__ import main as bstack1ll1lllll_opy_
  bstack1ll1lllll_opy_(arg)
def bstack1l1l11l1l_opy_():
  logger.info(bstack11llllll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫഐ"), help=bstack1l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ഑"))
  parser.add_argument(bstack1l_opy_ (u"ࠧ࠮ࡷࠪഒ"), bstack1l_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬഓ"), help=bstack1l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨഔ"))
  parser.add_argument(bstack1l_opy_ (u"ࠪ࠱ࡰ࠭ക"), bstack1l_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪഖ"), help=bstack1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ഗ"))
  parser.add_argument(bstack1l_opy_ (u"࠭࠭ࡧࠩഘ"), bstack1l_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬങ"), help=bstack1l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧച"))
  bstack11l1l1ll1_opy_ = parser.parse_args()
  try:
    bstack1l111lll_opy_ = bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ഛ")
    if bstack11l1l1ll1_opy_.framework and bstack11l1l1ll1_opy_.framework not in (bstack1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪജ"), bstack1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬഝ")):
      bstack1l111lll_opy_ = bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫഞ")
    bstack1llll1ll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l111lll_opy_)
    bstack1lll1111_opy_ = open(bstack1llll1ll_opy_, bstack1l_opy_ (u"࠭ࡲࠨട"))
    bstack1ll1111l1_opy_ = bstack1lll1111_opy_.read()
    bstack1lll1111_opy_.close()
    if bstack11l1l1ll1_opy_.username:
      bstack1ll1111l1_opy_ = bstack1ll1111l1_opy_.replace(bstack1l_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧഠ"), bstack11l1l1ll1_opy_.username)
    if bstack11l1l1ll1_opy_.key:
      bstack1ll1111l1_opy_ = bstack1ll1111l1_opy_.replace(bstack1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪഡ"), bstack11l1l1ll1_opy_.key)
    if bstack11l1l1ll1_opy_.framework:
      bstack1ll1111l1_opy_ = bstack1ll1111l1_opy_.replace(bstack1l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪഢ"), bstack11l1l1ll1_opy_.framework)
    file_name = bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ണ")
    file_path = os.path.abspath(file_name)
    bstack1l1ll111_opy_ = open(file_path, bstack1l_opy_ (u"ࠫࡼ࠭ത"))
    bstack1l1ll111_opy_.write(bstack1ll1111l1_opy_)
    bstack1l1ll111_opy_.close()
    logger.info(bstack1l1l1l1ll_opy_)
    try:
      os.environ[bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧഥ")] = bstack11l1l1ll1_opy_.framework if bstack11l1l1ll1_opy_.framework != None else bstack1l_opy_ (u"ࠨࠢദ")
      config = yaml.safe_load(bstack1ll1111l1_opy_)
      config[bstack1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧധ")] = bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧന")
      bstack1l1111ll_opy_(bstack11ll1l11l_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1lll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11lll111_opy_.format(str(e)))
def bstack1l1111ll_opy_(bstack1111l_opy_, config, bstack111l11ll_opy_ = {}):
  global bstack11lll1_opy_
  if not config:
    return
  bstack11ll111_opy_ = bstack1l111ll11_opy_ if not bstack11lll1_opy_ else ( bstack1lll11111_opy_ if bstack1l_opy_ (u"ࠩࡤࡴࡵ࠭ഩ") in config else bstack11lll111l_opy_ )
  data = {
    bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬപ"): config[bstack1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ഫ")],
    bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨബ"): config[bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩഭ")],
    bstack1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫമ"): bstack1111l_opy_,
    bstack1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫയ"): {
      bstack1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧര"): str(config[bstack1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪറ")]) if bstack1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫല") in config else bstack1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨള"),
      bstack1l_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨഴ"): bstack1l1l1_opy_(os.getenv(bstack1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤവ"), bstack1l_opy_ (u"ࠣࠤശ"))),
      bstack1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫഷ"): bstack1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪസ"),
      bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬഹ"): bstack11ll111_opy_,
      bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨഺ"): config[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦ഻ࠩ")]if config[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ഼ࠪ")] else bstack1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤഽ"),
      bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫാ"): str(config[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬി")]) if bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ീ") in config else bstack1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨു"),
      bstack1l_opy_ (u"࠭࡯ࡴࠩൂ"): sys.platform,
      bstack1l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩൃ"): socket.gethostname()
    }
  }
  update(data[bstack1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫൄ")], bstack111l11ll_opy_)
  try:
    response = bstack11ll1ll1l_opy_(bstack1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ൅"), bstack1ll1l1ll_opy_, data, config)
    if response:
      logger.debug(bstack11l1l1l11_opy_.format(bstack1111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11llll111_opy_.format(str(e)))
def bstack11ll1ll1l_opy_(type, url, data, config):
  bstack1llll11l_opy_ = bstack1ll1l1_opy_.format(url)
  proxy = bstack1ll1lll_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭െ")) or config.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨേ")):
    proxies = {
      bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫൈ"): proxy
    }
  if type == bstack1l_opy_ (u"࠭ࡐࡐࡕࡗࠫ൉"):
    response = requests.post(bstack1llll11l_opy_, json=data,
                    headers={bstack1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ൊ"): bstack1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫോ")}, auth=(config[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫൌ")], config[bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ്࠭")]), proxies=proxies)
  return response
def bstack1l1l1_opy_(framework):
  return bstack1l_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣൎ").format(str(framework), __version__) if framework else bstack1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ൏").format(__version__)
def bstack11llll11_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack11ll1ll1_opy_()
    logger.debug(bstack1ll1l1lll_opy_.format(str(CONFIG)))
    bstack11ll11111_opy_()
    bstack11lllll_opy_()
  except Exception as e:
    logger.error(bstack1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥ൐") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11l1ll11l_opy_
  atexit.register(bstack1l1l1ll1_opy_)
  signal.signal(signal.SIGINT, bstack1ll1l1ll1_opy_)
  signal.signal(signal.SIGTERM, bstack1ll1l1ll1_opy_)
def bstack11l1ll11l_opy_(exctype, value, traceback):
  global bstack1l1ll1_opy_
  try:
    for driver in bstack1l1ll1_opy_:
      driver.execute_script(
        bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧ൑") + json.dumps(bstack1l_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ൒") + str(value)) + bstack1l_opy_ (u"ࠩࢀࢁࠬ൓"))
  except Exception:
    pass
  bstack1l1111l1l_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1111l1l_opy_(message = bstack1l_opy_ (u"ࠪࠫൔ")):
  global CONFIG
  try:
    if message:
      bstack111l11ll_opy_ = {
        bstack1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪൕ"): str(message)
      }
      bstack1l1111ll_opy_(bstack11l111l_opy_, CONFIG, bstack111l11ll_opy_)
    else:
      bstack1l1111ll_opy_(bstack11l111l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lll1llll_opy_.format(str(e)))
def bstack11l1l11ll_opy_(bstack1111llll_opy_, size):
  bstack1l1111l1_opy_ = []
  while len(bstack1111llll_opy_) > size:
    bstack11lllllll_opy_ = bstack1111llll_opy_[:size]
    bstack1l1111l1_opy_.append(bstack11lllllll_opy_)
    bstack1111llll_opy_   = bstack1111llll_opy_[size:]
  bstack1l1111l1_opy_.append(bstack1111llll_opy_)
  return bstack1l1111l1_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack111l1111_opy_)
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨൖ")  or sys.argv[1] == bstack1l_opy_ (u"࠭࠭ࡷࠩൗ"):
    logger.info(bstack1l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧ൘").format(__version__))
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ൙"):
    bstack1l1l11l1l_opy_()
    return
  args = sys.argv
  bstack11llll11_opy_()
  global CONFIG
  global bstack1l111ll1l_opy_
  global bstack1l11l111_opy_
  global bstack1l1l1lll1_opy_
  global bstack1ll1l_opy_
  global bstack1l11ll_opy_
  bstack111lll1_opy_ = bstack1l_opy_ (u"ࠩࠪ൚")
  if args[1] == bstack1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ൛") or args[1] == bstack1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ൜"):
    bstack111lll1_opy_ = bstack1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൝")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ൞"):
    bstack111lll1_opy_ = bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ൟ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧൠ"):
    bstack111lll1_opy_ = bstack1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨൡ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൢ"):
    bstack111lll1_opy_ = bstack1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬൣ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൤"):
    bstack111lll1_opy_ = bstack1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൥")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ൦"):
    bstack111lll1_opy_ = bstack1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ൧")
    args = args[2:]
  else:
    if not bstack1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൨") in CONFIG or str(CONFIG[bstack1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൩")]).lower() in [bstack1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ൪"), bstack1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭൫")]:
      bstack111lll1_opy_ = bstack1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൬")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ൭")]).lower() == bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൮"):
      bstack111lll1_opy_ = bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൯")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൰")]).lower() == bstack1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൱"):
      bstack111lll1_opy_ = bstack1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൲")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ൳")]).lower() == bstack1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൴"):
      bstack111lll1_opy_ = bstack1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ൵")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൶")]).lower() == bstack1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ൷"):
      bstack111lll1_opy_ = bstack1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൸")
      args = args[1:]
    else:
      os.environ[bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൹")] = bstack111lll1_opy_
      bstack1l111llll_opy_(bstack1l1l1l11l_opy_)
  global bstack1l1l11ll1_opy_
  try:
    os.environ[bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨൺ")] = bstack111lll1_opy_
    bstack1l1111ll_opy_(bstack1llll1ll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lll1llll_opy_.format(str(e)))
  global bstack1l111l_opy_
  global bstack1l1l1ll_opy_
  global bstack1ll11l11_opy_
  global bstack1llll111l_opy_
  global bstack11lllll1_opy_
  global bstack11lll1l1l_opy_
  global bstack11llll11l_opy_
  global bstack111ll1l_opy_
  global bstack1l1ll11_opy_
  global bstack11111ll_opy_
  global bstack11ll11l_opy_
  global bstack1ll11l1l1_opy_
  global bstack1l11lllll_opy_
  global bstack1l1l1ll1l_opy_
  global bstack11l11_opy_
  global bstack1l11l1ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l111l_opy_ = webdriver.Remote.__init__
    bstack1l1ll11_opy_ = WebDriver.close
    bstack1ll11l1l1_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1l11ll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack11l11l1l_opy_():
    if bstack11lll1ll1_opy_() < version.parse(bstack1ll1111_opy_):
      logger.error(bstack11ll1lll_opy_.format(bstack11lll1ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l11lllll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll111l1_opy_.format(str(e)))
  bstack1llllll1_opy_()
  if (bstack111lll1_opy_ in [bstack1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ൻ"), bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧർ"), bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪൽ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll1l11ll_opy_
        bstack1ll11l11_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1ll11l1_opy_ + str(e))
    except Exception as e:
      bstack11l11ll_opy_(e, bstack1l1ll11l1_opy_)
    if bstack111lll1_opy_ != bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൾ"):
      bstack11l1llll1_opy_()
    bstack1l1l1ll_opy_ = Output.end_test
    bstack1llll111l_opy_ = TestStatus.__init__
    bstack11lll1l1l_opy_ = pabot._run
    bstack11llll11l_opy_ = QueueItem.__init__
    bstack111ll1l_opy_ = pabot._create_command_for_execution
    bstack1l11l1ll1_opy_ = pabot._report_results
  if bstack111lll1_opy_ == bstack1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫൿ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l11ll_opy_(e, bstack1ll111l11_opy_)
    bstack11111ll_opy_ = Runner.run_hook
    bstack11ll11l_opy_ = Step.run
  if bstack111lll1_opy_ == bstack1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ඀"):
    try:
      from _pytest.config import Config
      bstack1l1l1ll1l_opy_ = Config.getoption
      from _pytest import runner
      bstack11l11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l11lll1_opy_)
  if bstack111lll1_opy_ == bstack1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඁ"):
    bstack11lll1l1_opy_()
    bstack1ll1l11l_opy_()
    if bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪං") in CONFIG:
      bstack1l11l111_opy_ = True
      bstack11ll1111_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫඃ")]):
        bstack11ll1111_opy_.append(bstack1l1l1111_opy_(name=str(index),
                                      target=bstack11lllll11_opy_, args=(args[0], index)))
      for t in bstack11ll1111_opy_:
        t.start()
      for t in bstack11ll1111_opy_:
        t.join()
    else:
      bstack1111l1l1_opy_(bstack1lllll111_opy_)
      exec(open(args[0]).read())
  elif bstack111lll1_opy_ == bstack1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ඄") or bstack111lll1_opy_ == bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩඅ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l11ll_opy_(e, bstack1l1ll11l1_opy_)
    bstack11lll1l1_opy_()
    bstack1111l1l1_opy_(bstack1l1ll_opy_)
    if bstack1l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩආ") in args:
      i = args.index(bstack1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪඇ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l111ll1l_opy_))
    args.insert(0, str(bstack1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫඈ")))
    pabot.main(args)
  elif bstack111lll1_opy_ == bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඉ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l11ll_opy_(e, bstack1l1ll11l1_opy_)
    for a in args:
      if bstack1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧඊ") in a:
        bstack1l1l1lll1_opy_ = int(a.split(bstack1l_opy_ (u"ࠩ࠽ࠫඋ"))[1])
      if bstack1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧඌ") in a:
        bstack1ll1l_opy_ = str(a.split(bstack1l_opy_ (u"ࠫ࠿࠭ඍ"))[1])
      if bstack1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬඎ") in a:
        bstack1l11ll_opy_ = str(a.split(bstack1l_opy_ (u"࠭࠺ࠨඏ"))[1])
    bstack1l11l1l1l_opy_ = None
    if bstack1l_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ඐ") in args:
      i = args.index(bstack1l_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧඑ"))
      args.pop(i)
      bstack1l11l1l1l_opy_ = args.pop(i)
    if bstack1l11l1l1l_opy_ is not None:
      global bstack1l111l111_opy_
      bstack1l111l111_opy_ = bstack1l11l1l1l_opy_
    bstack1111l1l1_opy_(bstack1l1ll_opy_)
    run_cli(args)
  elif bstack111lll1_opy_ == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩඒ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack1lll1111l_opy_ = importlib.find_loader(bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬඓ"))
    except Exception as e:
      logger.warn(e, bstack1l11lll1_opy_)
    bstack11lll1l1_opy_()
    try:
      if bstack1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ඔ") in args:
        i = args.index(bstack1l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧඕ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩඖ") in args:
        i = args.index(bstack1l_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ඗"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠨ࠯ࡳࠫ඘") in args:
        i = args.index(bstack1l_opy_ (u"ࠩ࠰ࡴࠬ඙"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫක") in args:
        i = args.index(bstack1l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬඛ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠬ࠳࡮ࠨග") in args:
        i = args.index(bstack1l_opy_ (u"࠭࠭࡯ࠩඝ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack111llll1_opy_ = config.args
    bstack1llll1l_opy_ = config.invocation_params.args
    bstack1llll1l_opy_ = list(bstack1llll1l_opy_)
    bstack1ll111ll1_opy_ = []
    for arg in bstack1llll1l_opy_:
      for spec in bstack111llll1_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1ll111ll1_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨඞ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111llll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l11l11_opy_)))
                    for bstack1l1l11l11_opy_ in bstack111llll1_opy_]
    if (bstack1111l11_opy_):
      bstack1ll111ll1_opy_.append(bstack1l_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬඟ"))
      bstack1ll111ll1_opy_.append(bstack1l_opy_ (u"ࠩࡗࡶࡺ࡫ࠧච"))
    bstack1ll111ll1_opy_.append(bstack1l_opy_ (u"ࠪ࠱ࡵ࠭ඡ"))
    bstack1ll111ll1_opy_.append(bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩජ"))
    bstack1ll111ll1_opy_.append(bstack1l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧඣ"))
    bstack1ll111ll1_opy_.append(bstack1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ඤ"))
    bstack1l11111ll_opy_ = []
    for spec in bstack111llll1_opy_:
      bstack111llll_opy_ = []
      bstack111llll_opy_.append(spec)
      bstack111llll_opy_ += bstack1ll111ll1_opy_
      bstack1l11111ll_opy_.append(bstack111llll_opy_)
    bstack1l11l111_opy_ = True
    bstack1ll11l1l_opy_ = 1
    if bstack1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧඥ") in CONFIG:
      bstack1ll11l1l_opy_ = CONFIG[bstack1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨඦ")]
    bstack1ll1l1l1l_opy_ = int(bstack1ll11l1l_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬට")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ඨ")]):
      for bstack111llll_opy_ in bstack1l11111ll_opy_:
        item = {}
        item[bstack1l_opy_ (u"ࠫࡦࡸࡧࠨඩ")] = bstack111llll_opy_
        item[bstack1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫඪ")] = index
        execution_items.append(item)
    bstack1lllll1l1_opy_ = bstack11l1l11ll_opy_(execution_items, bstack1ll1l1l1l_opy_)
    for execution_item in bstack1lllll1l1_opy_:
      bstack11ll1111_opy_ = []
      for item in execution_item:
        bstack11ll1111_opy_.append(bstack1l1l1111_opy_(name=str(item[bstack1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬණ")]),
                                            target=bstack1l1l1l1l_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠧࡢࡴࡪࠫඬ")],)))
      for t in bstack11ll1111_opy_:
        t.start()
      for t in bstack11ll1111_opy_:
        t.join()
  elif bstack111lll1_opy_ == bstack1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨත"):
    try:
      from behave.__main__ import main as bstack1ll1lllll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l11ll_opy_(e, bstack1ll111l11_opy_)
    bstack11lll1l1_opy_()
    bstack1l11l111_opy_ = True
    bstack1ll11l1l_opy_ = 1
    if bstack1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩථ") in CONFIG:
      bstack1ll11l1l_opy_ = CONFIG[bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪද")]
    bstack1ll1l1l1l_opy_ = int(bstack1ll11l1l_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧධ")]))
    config = Configuration(args)
    bstack111llll1_opy_ = config.paths
    bstack11l1lll_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack111llll1_opy_:
        bstack11l1lll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭න"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111llll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l11l11_opy_)))
                    for bstack1l1l11l11_opy_ in bstack111llll1_opy_]
    bstack1l11111ll_opy_ = []
    for spec in bstack111llll1_opy_:
      bstack111llll_opy_ = []
      bstack111llll_opy_ += bstack11l1lll_opy_
      bstack111llll_opy_.append(spec)
      bstack1l11111ll_opy_.append(bstack111llll_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ඲")]):
      for bstack111llll_opy_ in bstack1l11111ll_opy_:
        item = {}
        item[bstack1l_opy_ (u"ࠧࡢࡴࡪࠫඳ")] = bstack1l_opy_ (u"ࠨࠢࠪප").join(bstack111llll_opy_)
        item[bstack1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨඵ")] = index
        execution_items.append(item)
    bstack1lllll1l1_opy_ = bstack11l1l11ll_opy_(execution_items, bstack1ll1l1l1l_opy_)
    for execution_item in bstack1lllll1l1_opy_:
      bstack11ll1111_opy_ = []
      for item in execution_item:
        bstack11ll1111_opy_.append(bstack1l1l1111_opy_(name=str(item[bstack1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩබ")]),
                                            target=bstack111lllll_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠫࡦࡸࡧࠨභ")],)))
      for t in bstack11ll1111_opy_:
        t.start()
      for t in bstack11ll1111_opy_:
        t.join()
  else:
    bstack1l111llll_opy_(bstack1l1l1l11l_opy_)
  bstack11111l_opy_()
def bstack11111l_opy_():
  [bstack1l11ll1l_opy_, bstack1ll111lll_opy_] = bstack111lll1l_opy_()
  if bstack1l11ll1l_opy_ is not None and bstack1l11ll1ll_opy_() != -1:
    sessions = bstack111l1ll1_opy_(bstack1l11ll1l_opy_)
    bstack1l111l1l_opy_(sessions, bstack1ll111lll_opy_)
def bstack1lllllll_opy_(bstack1l1lll11l_opy_):
    if bstack1l1lll11l_opy_:
        return bstack1l1lll11l_opy_.capitalize()
    else:
        return bstack1l1lll11l_opy_
def bstack1l1llll11_opy_(bstack1111ll1l_opy_):
    if bstack1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪම") in bstack1111ll1l_opy_ and bstack1111ll1l_opy_[bstack1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫඹ")] != bstack1l_opy_ (u"ࠧࠨය"):
        return bstack1111ll1l_opy_[bstack1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ර")]
    else:
        bstack1l1llll1l_opy_ = bstack1l_opy_ (u"ࠤࠥ඼")
        if bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪල") in bstack1111ll1l_opy_ and bstack1111ll1l_opy_[bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ඾")] != None:
            bstack1l1llll1l_opy_ += bstack1111ll1l_opy_[bstack1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ඿")] + bstack1l_opy_ (u"ࠨࠬࠡࠤව")
            if bstack1111ll1l_opy_[bstack1l_opy_ (u"ࠧࡰࡵࠪශ")] == bstack1l_opy_ (u"ࠣ࡫ࡲࡷࠧෂ"):
                bstack1l1llll1l_opy_ += bstack1l_opy_ (u"ࠤ࡬ࡓࡘࠦࠢස")
            bstack1l1llll1l_opy_ += (bstack1111ll1l_opy_[bstack1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧහ")] or bstack1l_opy_ (u"ࠫࠬළ"))
            return bstack1l1llll1l_opy_
        else:
            bstack1l1llll1l_opy_ += bstack1lllllll_opy_(bstack1111ll1l_opy_[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ෆ")]) + bstack1l_opy_ (u"ࠨࠠࠣ෇") + (bstack1111ll1l_opy_[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ෈")] or bstack1l_opy_ (u"ࠨࠩ෉")) + bstack1l_opy_ (u"ࠤ࠯ࠤ්ࠧ")
            if bstack1111ll1l_opy_[bstack1l_opy_ (u"ࠪࡳࡸ࠭෋")] == bstack1l_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧ෌"):
                bstack1l1llll1l_opy_ += bstack1l_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥ෍")
            bstack1l1llll1l_opy_ += bstack1111ll1l_opy_[bstack1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ෎")] or bstack1l_opy_ (u"ࠧࠨා")
            return bstack1l1llll1l_opy_
def bstack11l1l1l_opy_(bstack1l11l11l1_opy_):
    if bstack1l11l11l1_opy_ == bstack1l_opy_ (u"ࠣࡦࡲࡲࡪࠨැ"):
        return bstack1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬෑ")
    elif bstack1l11l11l1_opy_ == bstack1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥි"):
        return bstack1l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧී")
    elif bstack1l11l11l1_opy_ == bstack1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧු"):
        return bstack1l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭෕")
    elif bstack1l11l11l1_opy_ == bstack1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨූ"):
        return bstack1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ෗")
    elif bstack1l11l11l1_opy_ == bstack1l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥෘ"):
        return bstack1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨෙ")
    elif bstack1l11l11l1_opy_ == bstack1l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧේ"):
        return bstack1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ෛ")
    else:
        return bstack1l_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪො")+bstack1lllllll_opy_(bstack1l11l11l1_opy_)+bstack1l_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ෝ")
def bstack11l1l1_opy_(session):
    return bstack1l_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨෞ").format(session[bstack1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ෟ")],bstack1l1llll11_opy_(session), bstack11l1l1l_opy_(session[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩ෠")]), bstack11l1l1l_opy_(session[bstack1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ෡")]), bstack1lllllll_opy_(session[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭෢")] or session[bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭෣")] or bstack1l_opy_ (u"ࠧࠨ෤")) + bstack1l_opy_ (u"ࠣࠢࠥ෥") + (session[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ෦")] or bstack1l_opy_ (u"ࠪࠫ෧")), session[bstack1l_opy_ (u"ࠫࡴࡹࠧ෨")] + bstack1l_opy_ (u"ࠧࠦࠢ෩") + session[bstack1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ෪")], session[bstack1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ෫")] or bstack1l_opy_ (u"ࠨࠩ෬"), session[bstack1l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭෭")] if session[bstack1l_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧ෮")] else bstack1l_opy_ (u"ࠫࠬ෯"))
def bstack1l111l1l_opy_(sessions, bstack1ll111lll_opy_):
  try:
    bstack1111l111_opy_ = bstack1l_opy_ (u"ࠧࠨ෰")
    if not os.path.exists(bstack1ll11l111_opy_):
      os.mkdir(bstack1ll11l111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ෱")), bstack1l_opy_ (u"ࠧࡳࠩෲ")) as f:
      bstack1111l111_opy_ = f.read()
    bstack1111l111_opy_ = bstack1111l111_opy_.replace(bstack1l_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬෳ"), str(len(sessions)))
    bstack1111l111_opy_ = bstack1111l111_opy_.replace(bstack1l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩ෴"), bstack1ll111lll_opy_)
    bstack1111l111_opy_ = bstack1111l111_opy_.replace(bstack1l_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫ෵"), sessions[0].get(bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨ෶")) if sessions[0] else bstack1l_opy_ (u"ࠬ࠭෷"))
    with open(os.path.join(bstack1ll11l111_opy_, bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ෸")), bstack1l_opy_ (u"ࠧࡸࠩ෹")) as stream:
      stream.write(bstack1111l111_opy_.split(bstack1l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬ෺"))[0])
      for session in sessions:
        stream.write(bstack11l1l1_opy_(session))
      stream.write(bstack1111l111_opy_.split(bstack1l_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭෻"))[1])
    logger.info(bstack1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭෼").format(bstack1ll11l111_opy_));
  except Exception as e:
    logger.debug(bstack1ll111ll_opy_.format(str(e)))
def bstack111l1ll1_opy_(bstack1l11ll1l_opy_):
  global CONFIG
  try:
    host = bstack1l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧ෽") if bstack1l_opy_ (u"ࠬࡧࡰࡱࠩ෾") in CONFIG else bstack1l_opy_ (u"࠭ࡡࡱ࡫ࠪ෿")
    user = CONFIG[bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ฀")]
    key = CONFIG[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫก")]
    bstack1lll1l_opy_ = bstack1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨข") if bstack1l_opy_ (u"ࠪࡥࡵࡶࠧฃ") in CONFIG else bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ค")
    url = bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪฅ").format(user, key, host, bstack1lll1l_opy_, bstack1l11ll1l_opy_)
    headers = {
      bstack1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬฆ"): bstack1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪง"),
    }
    proxy = bstack1ll1lll_opy_(CONFIG)
    proxies = {}
    if CONFIG.get(bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫจ")) or CONFIG.get(bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ฉ")):
      proxies = {
        bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩช"): proxy
      }
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩซ")], response.json()))
  except Exception as e:
    logger.debug(bstack1111lll1_opy_.format(str(e)))
def bstack111lll1l_opy_():
  global CONFIG
  try:
    if bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨฌ") in CONFIG:
      host = bstack1l_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩญ") if bstack1l_opy_ (u"ࠧࡢࡲࡳࠫฎ") in CONFIG else bstack1l_opy_ (u"ࠨࡣࡳ࡭ࠬฏ")
      user = CONFIG[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫฐ")]
      key = CONFIG[bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ฑ")]
      bstack1lll1l_opy_ = bstack1l_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪฒ") if bstack1l_opy_ (u"ࠬࡧࡰࡱࠩณ") in CONFIG else bstack1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨด")
      url = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧต").format(user, key, host, bstack1lll1l_opy_)
      headers = {
        bstack1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧถ"): bstack1l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬท"),
      }
      if bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬธ") in CONFIG:
        params = {bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩน"):CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨบ")], bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩป"):CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩผ")]}
      else:
        params = {bstack1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ฝ"):CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬพ")]}
      proxy = bstack1ll1lll_opy_(CONFIG)
      proxies = {}
      if CONFIG.get(bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ฟ")) or CONFIG.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨภ")):
        proxies = {
          bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫม"): proxy
        }
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1l111l11l_opy_ = response.json()[0][bstack1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩย")]
        if bstack1l111l11l_opy_:
          bstack1ll111lll_opy_ = bstack1l111l11l_opy_[bstack1l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫร")].split(bstack1l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧฤ"))[0] + bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪล") + bstack1l111l11l_opy_[bstack1l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ฦ")]
          logger.info(bstack11l111ll_opy_.format(bstack1ll111lll_opy_))
          bstack11lll_opy_ = CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧว")]
          if bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧศ") in CONFIG:
            bstack11lll_opy_ += bstack1l_opy_ (u"࠭ࠠࠨษ") + CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩส")]
          if bstack11lll_opy_!= bstack1l111l11l_opy_[bstack1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ห")]:
            logger.debug(bstack11ll111l_opy_.format(bstack1l111l11l_opy_[bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧฬ")], bstack11lll_opy_))
          return [bstack1l111l11l_opy_[bstack1l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭อ")], bstack1ll111lll_opy_]
    else:
      logger.warn(bstack1l11lll_opy_)
  except Exception as e:
    logger.debug(bstack111l1ll_opy_.format(str(e)))
  return [None, None]
def bstack1l1l111l1_opy_(url, bstack1lllll11l_opy_=False):
  global CONFIG
  global bstack1lllllll1_opy_
  if not bstack1lllllll1_opy_:
    hostname = bstack1l11ll11_opy_(url)
    is_private = bstack1l1l11l_opy_(hostname)
    if (bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨฮ") in CONFIG and not CONFIG[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩฯ")]) and (is_private or bstack1lllll11l_opy_):
      bstack1lllllll1_opy_ = hostname
def bstack1l11ll11_opy_(url):
  return urlparse(url).hostname
def bstack1l1l11l_opy_(hostname):
  for bstack11l1ll111_opy_ in bstack1l11lll11_opy_:
    regex = re.compile(bstack11l1ll111_opy_)
    if regex.match(hostname):
      return True
  return False