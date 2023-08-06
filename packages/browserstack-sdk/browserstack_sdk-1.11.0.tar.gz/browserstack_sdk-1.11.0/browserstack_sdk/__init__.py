# coding: UTF-8
import sys
bstackl_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstack1_opy_ = 7
def bstack1l_opy_ (bstack1ll1_opy_):
    global bstack1l1_opy_
    stringNr = ord (bstack1ll1_opy_ [-1])
    bstack1ll_opy_ = bstack1ll1_opy_ [:-1]
    bstack11l_opy_ = stringNr % len (bstack1ll_opy_)
    bstack111_opy_ = bstack1ll_opy_ [:bstack11l_opy_] + bstack1ll_opy_ [bstack11l_opy_:]
    if bstackl_opy_:
        bstack1l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack1lll_opy_ + stringNr) % bstack1_opy_) for bstack1lll_opy_, char in enumerate (bstack111_opy_)])
    else:
        bstack1l1l_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack1lll_opy_ + stringNr) % bstack1_opy_) for bstack1lll_opy_, char in enumerate (bstack111_opy_)])
    return eval (bstack1l1l_opy_)
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
bstack11l1ll1ll_opy_ = {
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
bstack1l1ll11l_opy_ = [
  bstack1l_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstack1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstack1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1lll1l11l_opy_ = {
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
bstack1l1llll1l_opy_ = {
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
bstack1ll1111_opy_ = {
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
bstack1ll1l11l_opy_ = [
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
bstack11l1ll1l1_opy_ = [
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
bstack11l1l11l_opy_ = [
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
bstack11lll111_opy_ = {
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
bstack1l11_opy_ = bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack11ll1ll11_opy_ = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack11ll111l_opy_ = bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack1l11l1l_opy_ = {
  bstack1l_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack1l_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack1l_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1l1l1lll1_opy_ = bstack1l11l1l_opy_[bstack1l_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack1lll1_opy_ = bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack11lll1l1l_opy_ = bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1ll1111ll_opy_ = bstack1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack11ll1111l_opy_ = bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack11111lll_opy_ = [bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack1l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack1l11l1l1l_opy_ = [bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack11l11ll1_opy_ = [
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
bstack1lllllll1_opy_ = bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack11l1ll_opy_ = [bstack1l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack1l_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack1l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1lll1ll11_opy_ = [bstack1l_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack1l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack11l11l_opy_ = {
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack1l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack1l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack11l1lll11_opy_ = [
  bstack1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1l1l11_opy_ = bstack11l1ll1l1_opy_ + bstack11l1l11l_opy_ + bstack11l11ll1_opy_
bstack1l111l1l1_opy_ = [
  bstack1l_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack1l_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack1l_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack1l_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack1l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack1l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack1l_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack1ll1ll1ll_opy_ = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack1ll11lll1_opy_ = bstack1l_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack11ll1l1_opy_ = [ bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack1ll1l11_opy_ = [ bstack1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack111111_opy_ = [ bstack1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack11lll1l11_opy_ = bstack1l_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack111l1ll_opy_ = bstack1l_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack11l1l1ll1_opy_ = bstack1l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack11ll1111_opy_ = bstack1l_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack1ll1llll_opy_ = [
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
bstack111l111_opy_ = bstack1l_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧਧ")
def bstack1lll1l_opy_():
  global CONFIG
  headers = {
        bstack1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਨ"): bstack1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ਩"),
      }
  proxy = bstack1ll11111l_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨਪ")) or CONFIG.get(bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪਫ")):
    proxies = {
      bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ਬ"): proxy
    }
  try:
    response = requests.get(bstack11ll111l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1ll1lll1l_opy_ = response.json()[bstack1l_opy_ (u"ࠨࡪࡸࡦࡸ࠭ਭ")]
      logger.debug(bstack1111ll1l_opy_.format(response.json()))
      return bstack1ll1lll1l_opy_
    else:
      logger.debug(bstack11lllll1_opy_.format(bstack1l_opy_ (u"ࠤࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡥࠡࡧࡵࡶࡴࡸࠠࠣਮ")))
  except Exception as e:
    logger.debug(bstack11lllll1_opy_.format(e))
def bstack1ll111ll_opy_(hub_url):
  global CONFIG
  url = bstack1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧਯ")+  hub_url + bstack1l_opy_ (u"ࠦ࠴ࡩࡨࡦࡥ࡮ࠦਰ")
  headers = {
        bstack1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ਱"): bstack1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩਲ"),
      }
  proxy = bstack1ll11111l_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪਲ਼")) or CONFIG.get(bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ਴")):
    proxies = {
      bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨਵ"): proxy
    }
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1111111_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11ll111_opy_.format(hub_url, e))
def bstack111l1ll1_opy_():
  try:
    global bstack1l1ll1ll1_opy_
    bstack1ll1lll1l_opy_ = bstack1lll1l_opy_()
    with Pool() as pool:
      results = pool.map(bstack1ll111ll_opy_, bstack1ll1lll1l_opy_)
    bstack11lll11_opy_ = {}
    for item in results:
      hub_url = item[bstack1l_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫਸ਼")]
      latency = item[bstack1l_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬ਷")]
      bstack11lll11_opy_[hub_url] = latency
    bstack1l11l1_opy_ = min(bstack11lll11_opy_, key= lambda x: bstack11lll11_opy_[x])
    bstack1l1ll1ll1_opy_ = bstack1l11l1_opy_
    logger.debug(bstack11ll1lll1_opy_.format(bstack1l11l1_opy_))
  except Exception as e:
    logger.debug(bstack111l11l1_opy_.format(e))
bstack1ll1ll1_opy_ = bstack1l_opy_ (u"࡙ࠬࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠻ࠢࡾࢁࠬਸ")
bstack1l11l111l_opy_ = bstack1l_opy_ (u"࠭ࡃࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡶࡩࡹࡻࡰࠢࠩਹ")
bstack1ll11ll_opy_ = bstack1l_opy_ (u"ࠧࡑࡣࡵࡷࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩ਺")
bstack1111llll_opy_ = bstack1l_opy_ (u"ࠨࡕࡤࡲ࡮ࡺࡩࡻࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭਻")
bstack11l1111l_opy_ = bstack1l_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡪࡸࡦࠥࡻࡲ࡭࠼ࠣࡿࢂ਼࠭")
bstack1l1111lll_opy_ = bstack1l_opy_ (u"ࠪࡗࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࡼࡿࠪ਽")
bstack1l11l1l11_opy_ = bstack1l_opy_ (u"ࠫࡗ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡩ࡯ࡶࡨࡶࡷࡻࡰࡵ࠮ࠣࡩࡽ࡯ࡴࡪࡰࡪࠫਾ")
bstack1ll1llll1_opy_ = bstack1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪਿ")
bstack1ll1l1l11_opy_ = bstack1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡢࡰࡧࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫੀ")
bstack111lll_opy_ = bstack1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡴࡲࡦࡴࡺࠬࠡࡲࡤࡦࡴࡺࠠࡢࡰࡧࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡲࡩࡣࡴࡤࡶࡾࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡶࡲࠤࡷࡻ࡮ࠡࡴࡲࡦࡴࡺࠠࡵࡧࡶࡸࡸࠦࡩ࡯ࠢࡳࡥࡷࡧ࡬࡭ࡧ࡯࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠳ࡰࡢࡤࡲࡸࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࡡࠩੁ")
bstack1llll1l1_opy_ = bstack1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡥࡩ࡭ࡧࡶࡦࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࡡࠩੂ")
bstack1l11lll11_opy_ = bstack1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡥࡵࡶࡩࡶ࡯࠰ࡧࡱ࡯ࡥ࡯ࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡄࡴࡵ࡯ࡵ࡮࠯ࡓࡽࡹ࡮࡯࡯࠯ࡆࡰ࡮࡫࡮ࡵࡢࠪ੃")
bstack11lll111l_opy_ = bstack1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡤࠬ੄")
bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡧ࡫ࡱࡨࠥ࡫ࡩࡵࡪࡨࡶ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡰࡴࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡷࡥࡱࡲࠠࡵࡪࡨࠤࡷ࡫࡬ࡦࡸࡤࡲࡹࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡷࡶ࡭ࡳ࡭ࠠࡱ࡫ࡳࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠫ੅")
bstack1ll11llll_opy_ = bstack1l_opy_ (u"ࠬࡎࡡ࡯ࡦ࡯࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥ࡯ࡳࡸ࡫ࠧ੆")
bstack1l1l11111_opy_ = bstack1l_opy_ (u"࠭ࡁ࡭࡮ࠣࡨࡴࡴࡥࠢࠩੇ")
bstack1llllll_opy_ = bstack1l_opy_ (u"ࠧࡄࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࠦࡡࡵࠢࡤࡲࡾࠦࡰࡢࡴࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡲࡪࠥࠨࡻࡾࠤ࠱ࠤࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡧࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮࠲ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠠࡧ࡫࡯ࡩࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡴࡦࡵࡷࡷ࠳࠭ੈ")
bstack11l11111_opy_ = bstack1l_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡴࡨࡨࡪࡴࡴࡪࡣ࡯ࡷࠥࡴ࡯ࡵࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡷ࡬ࡪࡳࠠࡪࡰࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡦࡹࠠࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥࠤࡦࡴࡤࠡࠤࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠧࠦ࡯ࡳࠢࡶࡩࡹࠦࡴࡩࡧࡰࠤࡦࡹࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳ࠻ࠢࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦࠥࡧ࡮ࡥࠢࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞ࠨࠧ੉")
bstack11l1l1l11_opy_ = bstack1l_opy_ (u"ࠩࡐࡥࡱ࡬࡯ࡳ࡯ࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠦࢀࢃࠢࠨ੊")
bstack11l1ll11_opy_ = bstack1l_opy_ (u"ࠪࡉࡳࡩ࡯ࡶࡰࡷࡩࡷ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣ࠱ࠥࢁࡽࠨੋ")
bstack11l11l1l_opy_ = bstack1l_opy_ (u"ࠫࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫੌ")
bstack11l1111_opy_ = bstack1l_opy_ (u"࡙ࠬࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰ੍ࠬ")
bstack11llll11l_opy_ = bstack1l_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠤ࡮ࡹࠠ࡯ࡱࡺࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠦ࠭੎")
bstack1lll1l1ll_opy_ = bstack1l_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲ࠺ࠡࡽࢀࠫ੏")
bstack1llll1ll_opy_ = bstack1l_opy_ (u"ࠨࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡥ࡭ࡳࡧࡲࡺࠢࡺ࡭ࡹ࡮ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࡾࢁࠬ੐")
bstack11llllll_opy_ = bstack1l_opy_ (u"ࠩࡘࡴࡩࡧࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪੑ")
bstack1111ll11_opy_ = bstack1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠩ੒")
bstack1l1ll1ll_opy_ = bstack1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࠥࡧ࡮ࠡࡣࡳࡴࡷࡵࡰࡳ࡫ࡤࡸࡪࠦࡆࡘࠢࠫࡶࡴࡨ࡯ࡵ࠱ࡳࡥࡧࡵࡴࠪࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠯ࠤࡸࡱࡩࡱࠢࡷ࡬ࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡮ࡩࡾࠦࡩ࡯ࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡪࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡳࡪ࡯ࡳࡰࡪࠦࡰࡺࡶ࡫ࡳࡳࠦࡳࡤࡴ࡬ࡴࡹࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡢࡰࡼࠤࡋ࡝࠮ࠨ੓")
bstack1l1l11l1l_opy_ = bstack1l_opy_ (u"࡙ࠬࡥࡵࡶ࡬ࡲ࡬ࠦࡨࡵࡶࡳࡔࡷࡵࡸࡺ࠱࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡩࡵࡳࡴࡨࡲࡹࡲࡹࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࠬࢀࢃࠩ࠭ࠢࡳࡰࡪࡧࡳࡦࠢࡸࡴ࡬ࡸࡡࡥࡧࠣࡸࡴࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭࠿࠿࠷࠲࠵࠴࠰ࠡࡱࡵࠤࡷ࡫ࡦࡦࡴࠣࡸࡴࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠱ࡵࡹࡳ࠳ࡴࡦࡵࡷࡷ࠲ࡨࡥࡩ࡫ࡱࡨ࠲ࡶࡲࡰࡺࡼࠧࡵࡿࡴࡩࡱࡱࠤ࡫ࡵࡲࠡࡣࠣࡻࡴࡸ࡫ࡢࡴࡲࡹࡳࡪ࠮ࠨ੔")
bstack1ll11l11_opy_ = bstack1l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲࠳࠭੕")
bstack111lll1_opy_ = bstack1l_opy_ (u"ࠧࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡧࡦࡰࡨࡶࡦࡺࡥࡥࠢࡷ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠥࠬ੖")
bstack1ll1l1ll1_opy_ = bstack1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫࠮ࠡࡽࢀࠫ੗")
bstack11111l11_opy_ = bstack1l_opy_ (u"ࠩࡈࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡺࠠ࡭ࡧࡤࡷࡹࠦ࠱ࠡ࡫ࡱࡴࡺࡺࠬࠡࡴࡨࡧࡪ࡯ࡶࡦࡦࠣ࠴ࠬ੘")
bstack1ll1l1_opy_ = bstack1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡹࡷ࡯࡮ࡨࠢࡄࡴࡵࠦࡵࡱ࡮ࡲࡥࡩ࠴ࠠࡼࡿࠪਖ਼")
bstack1l11lll1_opy_ = bstack1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲ࡯ࡳࡦࡪࠠࡂࡲࡳ࠲ࠥࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࢀࢃ࠮ࠨਗ਼")
bstack1ll111l1_opy_ = bstack1l_opy_ (u"ࠬࡑࡥࡺࡵࠣࡧࡦࡴ࡮ࡰࡶࠣࡧࡴ࠳ࡥࡹ࡫ࡶࡸࠥࡧࡳࠡࡣࡳࡴࠥࡼࡡ࡭ࡷࡨࡷ࠱ࠦࡵࡴࡧࠣࡥࡳࡿࠠࡰࡰࡨࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࠦࡦࡳࡱࡰࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠮ࠣࡳࡳࡲࡹࠡࠤࡳࡥࡹ࡮ࠢࠡࡣࡱࡨࠥࠨࡣࡶࡵࡷࡳࡲࡥࡩࡥࠤࠣࡧࡦࡴࠠࡤࡱ࠰ࡩࡽ࡯ࡳࡵࠢࡷࡳ࡬࡫ࡴࡩࡧࡵ࠲ࠬਜ਼")
bstack1ll11_opy_ = bstack1l_opy_ (u"࡛࠭ࡊࡰࡹࡥࡱ࡯ࡤࠡࡣࡳࡴࠥࡶࡲࡰࡲࡨࡶࡹࡿ࡝ࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠡࡣࡵࡩࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠱ࠤࡋࡵࡲࠡ࡯ࡲࡶࡪࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡱ࡮ࡨࡥࡸ࡫ࠠࡷ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡰࡪࡷࡰ࠳ࡸ࡫ࡴ࠮ࡷࡳ࠱ࡹ࡫ࡳࡵࡵ࠲ࡷࡵ࡫ࡣࡪࡨࡼ࠱ࡦࡶࡰࠨੜ")
bstack1l1l1ll11_opy_ = bstack1l_opy_ (u"ࠧ࡜ࡋࡱࡺࡦࡲࡩࡥࠢࡤࡴࡵࠦࡰࡳࡱࡳࡩࡷࡺࡹ࡞ࠢࡖࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࡷࠥࡵࡦࠡࡣࡳࡴࠥࡧࡲࡦࠢࡲࡪࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠱ࠤࡋࡵࡲࠡ࡯ࡲࡶࡪࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡱ࡮ࡨࡥࡸ࡫ࠠࡷ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡰࡪࡷࡰ࠳ࡸ࡫ࡴ࠮ࡷࡳ࠱ࡹ࡫ࡳࡵࡵ࠲ࡷࡵ࡫ࡣࡪࡨࡼ࠱ࡦࡶࡰࠨ੝")
bstack1llll1ll1_opy_ = bstack1l_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡤࡴࡵࠦࡩࡥࠢࡾࢁࠥ࡬࡯ࡳࠢ࡫ࡥࡸ࡮ࠠ࠻ࠢࡾࢁ࠳࠭ਫ਼")
bstack11llll1l_opy_ = bstack1l_opy_ (u"ࠩࡄࡴࡵࠦࡕࡱ࡮ࡲࡥࡩ࡫ࡤࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠡࡋࡇࠤ࠿ࠦࡻࡾࠩ੟")
bstack111lll11_opy_ = bstack1l_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡄࡴࡵࠦ࠺ࠡࡽࢀ࠲ࠬ੠")
bstack1llllll1_opy_ = bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡱࡵࠤࡻࡧ࡮ࡪ࡮࡯ࡥࠥࡶࡹࡵࡪࡲࡲࠥࡺࡥࡴࡶࡶ࠰ࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡵࡧࡲࡢ࡮࡯ࡩࡱࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡁࠥ࠷ࠧ੡")
bstack11111_opy_ = bstack1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࠾ࠥࢁࡽࠨ੢")
bstack1111l1l_opy_ = bstack1l_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡦࡰࡴࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳ࠼ࠣࡿࢂ࠭੣")
bstack11l111l1_opy_ = bstack1l_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣ࡫ࡪࡺࠠࡳࡧࡤࡷࡴࡴࠠࡧࡱࡵࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪ࠴ࠠࡼࡿࠪ੤")
bstack1111l111_opy_ = bstack1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡢࡲ࡬ࠤࡨࡧ࡬࡭࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭੥")
bstack11l1l_opy_ = bstack1l_opy_ (u"ࠩࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡨࡰࡹࠣࡦࡺ࡯࡬ࡥࠢࡘࡖࡑ࠲ࠠࡢࡵࠣࡦࡺ࡯࡬ࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾࠦࡩࡴࠢࡱࡳࡹࠦࡵࡴࡧࡧ࠲ࠬ੦")
bstack1lll1111l_opy_ = bstack1l_opy_ (u"ࠪࡗࡪࡸࡶࡦࡴࠣࡷ࡮ࡪࡥࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠬࢀࢃࠩࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡤࡱࡪࠦࡡࡴࠢࡦࡰ࡮࡫࡮ࡵࠢࡶ࡭ࡩ࡫ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠫࡿࢂ࠯ࠧ੧")
bstack1ll1111l_opy_ = bstack1l_opy_ (u"࡛ࠫ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡨࡦࡹࡨࡣࡱࡤࡶࡩࡀࠠࡼࡿࠪ੨")
bstack1l1l1ll1l_opy_ = bstack1l_opy_ (u"࡛ࠬ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡣࡦࡧࡪࡹࡳࠡࡣࠣࡴࡷ࡯ࡶࡢࡶࡨࠤࡩࡵ࡭ࡢ࡫ࡱ࠾ࠥࢁࡽࠡ࠰ࠣࡗࡪࡺࠠࡵࡪࡨࠤ࡫ࡵ࡬࡭ࡱࡺ࡭ࡳ࡭ࠠࡤࡱࡱࡪ࡮࡭ࠠࡪࡰࠣࡽࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠼ࠣࡠࡳ࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯ࠣࡠࡳࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮࠽ࠤࡹࡸࡵࡦࠢ࡟ࡲ࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮ࠩ੩")
bstack111ll1ll_opy_ = bstack1l_opy_ (u"࠭ࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࡢࡩࡷࡸ࡯ࡳࠢ࠽ࠤࢀࢃࠧ੪")
bstack11ll11ll_opy_ = bstack1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡳࡪ࡟ࡢ࡯ࡳࡰ࡮ࡺࡵࡥࡧࡢࡩࡻ࡫࡮ࡵࠢࡩࡳࡷࠦࡓࡅࡍࡖࡩࡹࡻࡰࠡࡽࢀࠦ੫")
bstack1ll1ll1l1_opy_ = bstack1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠣࡿࢂࠨ੬")
bstack1lllll1l1_opy_ = bstack1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠥࢁࡽࠣ੭")
bstack1lllll1ll_opy_ = bstack1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬ࡩࡳࡧࡢࡶࡪࡷࡵࡦࡵࡷࠤࢀࢃࠢ੮")
bstack1l111ll11_opy_ = bstack1l_opy_ (u"ࠦࡕࡕࡓࡕࠢࡈࡺࡪࡴࡴࠡࡽࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦ࠺ࠡࡽࢀࠦ੯")
bstack1lll11_opy_ = bstack1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡵࡸ࡯ࡹࡻࠣࡷࡪࡺࡴࡪࡰࡪࡷ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩੰ")
bstack1111ll1l_opy_ = bstack1l_opy_ (u"࠭ࡒࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦ࠯࡯ࡧࡻࡸࡤ࡮ࡵࡣࡵࠣࡿࢂ࠭ੱ")
bstack11lllll1_opy_ = bstack1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣ࠳ࡳ࡫ࡸࡵࡡ࡫ࡹࡧࡹ࠺ࠡࡽࢀࠫੲ")
bstack11ll1lll1_opy_ = bstack1l_opy_ (u"ࠨࡐࡨࡥࡷ࡫ࡳࡵࠢ࡫ࡹࡧࠦࡡ࡭࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡷ࠿ࠦࡻࡾࠩੳ")
bstack111l11l1_opy_ = bstack1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࠡࡋࡑࠤࡆࡒࡌࡐࡅࡄࡘࡊࠦࡈࡖࡄࠣࡿࢂ࠭ੴ")
bstack1111111_opy_ = bstack1l_opy_ (u"ࠪࡐࡦࡺࡥ࡯ࡥࡼࠤࡴ࡬ࠠࡩࡷࡥ࠾ࠥࢁࡽࠡ࡫ࡶ࠾ࠥࢁࡽࠨੵ")
bstack11ll111_opy_ = bstack1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠ࡭ࡣࡷࡩࡳࡩࡹࠡࡨࡲࡶࠥࢁࡽࠡࡪࡸࡦ࠿ࠦࡻࡾࠩ੶")
bstack1l111111l_opy_ = bstack1l_opy_ (u"ࠬࡎࡵࡣࠢࡸࡶࡱࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡰࡲࡷ࡭ࡲࡧ࡬ࠡࡪࡸࡦ࠿ࠦࡻࡾࠩ੷")
bstack11l111ll_opy_ = bstack1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡲࡴࡹ࡯࡭ࡢ࡮ࠣ࡬ࡺࡨࠠࡶࡴ࡯࠾ࠥࢁࡽࠨ੸")
bstack1l1l1l111_opy_ = bstack1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡮࡬ࡷࡹࡹ࠺ࠡࡽࢀࠫ੹")
bstack11l1ll1l_opy_ = bstack1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠺ࠡࡽࢀࠫ੺")
bstack11l11ll_opy_ = bstack1l_opy_ (u"ࠩࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠢࠣ࡭࡫࠮ࡰࡢࡩࡨࠤࡂࡃ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠢࡾࡠࡳࠦࠠࠡࡶࡵࡽࢀࡢ࡮ࠡࡥࡲࡲࡸࡺࠠࡧࡵࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮࡜ࠨࡨࡶࡠࠬ࠯࠻࡝ࡰࠣࠤࠥࠦࠠࡧࡵ࠱ࡥࡵࡶࡥ࡯ࡦࡉ࡭ࡱ࡫ࡓࡺࡰࡦࠬࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩ࠮ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡵࡥࡩ࡯ࡦࡨࡼ࠮ࠦࠫࠡࠤ࠽ࠦࠥ࠱ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭࠮ࡡࡸࡣ࡬ࡸࠥࡴࡥࡸࡒࡤ࡫ࡪ࠸࠮ࡦࡸࡤࡰࡺࡧࡴࡦࠪࠥࠬ࠮ࠦ࠽࠿ࠢࡾࢁࠧ࠲ࠠ࡝ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠨࡽ࡝ࠩࠬ࠭࠮ࡡࠢࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠥࡡ࠮ࠦࠫࠡࠤ࠯ࡠࡡࡴࠢࠪ࡞ࡱࠤࠥࠦࠠࡾࡥࡤࡸࡨ࡮ࠨࡦࡺࠬࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡿ࡟ࡲࠥࠦ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠩ੻")
bstack1ll11l111_opy_ = bstack1l_opy_ (u"ࠪࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡢ࡮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡢ࡮ࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻࡝ࡰ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰࡯ࡥࡺࡴࡣࡩࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶ࠭ࠥࡃ࠾ࠡࡽ࡟ࡲࡱ࡫ࡴࠡࡥࡤࡴࡸࡁ࡜࡯ࡶࡵࡽࠥࢁ࡜࡯ࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࢃ࡜࡯ࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶࠫࡿࡡࡴࠠࠡࠢࠣࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺ࠺ࠡࡢࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠨࢀ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬࢁࡥ࠲࡜࡯ࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩ੼")
from ._version import __version__
bstack1l11l_opy_ = None
CONFIG = {}
bstack1l1llll11_opy_ = {}
bstack1l111l1l_opy_ = {}
bstack111ll1_opy_ = None
bstack1llll_opy_ = None
bstack1l1l111l1_opy_ = None
bstack1l1111ll1_opy_ = -1
bstack1l1l11l11_opy_ = bstack1l1l1lll1_opy_
bstack11l1ll11l_opy_ = 1
bstack11ll1l11l_opy_ = False
bstack11l1ll111_opy_ = bstack1l_opy_ (u"ࠫࠬ੽")
bstack1ll11l11l_opy_ = bstack1l_opy_ (u"ࠬ࠭੾")
bstack1lll11l1_opy_ = False
bstack1l111l11l_opy_ = True
bstack1l1l11ll_opy_ = bstack1l_opy_ (u"࠭ࠧ੿")
bstack11ll_opy_ = []
bstack1l1ll1ll1_opy_ = bstack1l_opy_ (u"ࠧࠨ઀")
bstack1l1l1l1l_opy_ = False
bstack1l1111111_opy_ = None
bstack1llllll11_opy_ = -1
bstack11lllll_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪઁ")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩં"), bstack1l_opy_ (u"ࠪ࠲ࡷࡵࡢࡰࡶ࠰ࡶࡪࡶ࡯ࡳࡶ࠰࡬ࡪࡲࡰࡦࡴ࠱࡮ࡸࡵ࡮ࠨઃ"))
bstack11llll_opy_ = False
bstack1ll111lll_opy_ = None
bstack111lll1l_opy_ = None
bstack1llll1111_opy_ = None
bstack11l1lll_opy_ = None
bstack1l11lllll_opy_ = None
bstack1l1l111l_opy_ = None
bstack1111l1_opy_ = None
bstack111l_opy_ = None
bstack1ll1l1ll_opy_ = None
bstack1ll111l_opy_ = None
bstack1ll1lllll_opy_ = None
bstack1l1111l_opy_ = None
bstack1ll111111_opy_ = None
bstack1ll1l11ll_opy_ = None
bstack1l11ll1ll_opy_ = None
bstack1l1l1111l_opy_ = bstack1l_opy_ (u"ࠦࠧ઄")
class bstack1l11l1ll_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1l11l1ll_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1l1l11l11_opy_,
                    format=bstack1l_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪઅ"),
                    datefmt=bstack1l_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨઆ"))
def bstack1ll11ll1l_opy_():
  global CONFIG
  global bstack1l1l11l11_opy_
  if bstack1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩઇ") in CONFIG:
    bstack1l1l11l11_opy_ = bstack1l11l1l_opy_[CONFIG[bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪઈ")]]
    logging.getLogger().setLevel(bstack1l1l11l11_opy_)
def bstack11l1l1111_opy_():
  global CONFIG
  global bstack11llll_opy_
  bstack111llll_opy_ = bstack1ll1lll11_opy_(CONFIG)
  if(bstack1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫઉ") in bstack111llll_opy_ and str(bstack111llll_opy_[bstack1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઊ")]).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩઋ")):
    bstack11llll_opy_ = True
def bstack111l1l11_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll11ll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1111ll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤઌ") == args[i].lower() or bstack1l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢઍ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l11ll_opy_
      bstack1l1l11ll_opy_ += bstack1l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ઎") + path
      return path
  return None
def bstack1l11ll_opy_():
  bstack1l1lll1_opy_ = bstack1l1111ll_opy_()
  if bstack1l1lll1_opy_ and os.path.exists(os.path.abspath(bstack1l1lll1_opy_)):
    fileName = bstack1l1lll1_opy_
  if bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬએ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ઐ")])) and not bstack1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬઑ") in locals():
    fileName = os.environ[bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ઒")]
  if bstack1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧઓ") in locals():
    bstack1llll1l11_opy_ = os.path.abspath(fileName)
  else:
    bstack1llll1l11_opy_ = bstack1l_opy_ (u"࠭ࠧઔ")
  bstack1ll1l1l1_opy_ = os.getcwd()
  bstack1lll11l1l_opy_ = bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪક")
  bstack111l1l1_opy_ = bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬખ")
  while (not os.path.exists(bstack1llll1l11_opy_)) and bstack1ll1l1l1_opy_ != bstack1l_opy_ (u"ࠤࠥગ"):
    bstack1llll1l11_opy_ = os.path.join(bstack1ll1l1l1_opy_, bstack1lll11l1l_opy_)
    if not os.path.exists(bstack1llll1l11_opy_):
      bstack1llll1l11_opy_ = os.path.join(bstack1ll1l1l1_opy_, bstack111l1l1_opy_)
    if bstack1ll1l1l1_opy_ != os.path.dirname(bstack1ll1l1l1_opy_):
      bstack1ll1l1l1_opy_ = os.path.dirname(bstack1ll1l1l1_opy_)
    else:
      bstack1ll1l1l1_opy_ = bstack1l_opy_ (u"ࠥࠦઘ")
  if not os.path.exists(bstack1llll1l11_opy_):
    bstack1l11l1lll_opy_(
      bstack1llllll_opy_.format(os.getcwd()))
  with open(bstack1llll1l11_opy_, bstack1l_opy_ (u"ࠫࡷ࠭ઙ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l11l1lll_opy_(bstack11l1l1l11_opy_.format(str(exc)))
def bstack11111l1_opy_(config):
  bstack1111111l_opy_ = bstack11lll11l_opy_(config)
  for option in list(bstack1111111l_opy_):
    if option.lower() in bstack11lll111_opy_ and option != bstack11lll111_opy_[option.lower()]:
      bstack1111111l_opy_[bstack11lll111_opy_[option.lower()]] = bstack1111111l_opy_[option]
      del bstack1111111l_opy_[option]
  return config
def bstack1l11lll_opy_():
  global bstack1l111l1l_opy_
  for key, bstack11lll1_opy_ in bstack1lll1l11l_opy_.items():
    if isinstance(bstack11lll1_opy_, list):
      for var in bstack11lll1_opy_:
        if var in os.environ:
          bstack1l111l1l_opy_[key] = os.environ[var]
          break
    elif bstack11lll1_opy_ in os.environ:
      bstack1l111l1l_opy_[key] = os.environ[bstack11lll1_opy_]
  if bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧચ") in os.environ:
    bstack1l111l1l_opy_[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪછ")] = {}
    bstack1l111l1l_opy_[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫજ")][bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪઝ")] = os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫઞ")]
def bstack11ll1l_opy_():
  global bstack1l1llll11_opy_
  global bstack1l1l11ll_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1l_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ટ").lower() == val.lower():
      bstack1l1llll11_opy_[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨઠ")] = {}
      bstack1l1llll11_opy_[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩડ")][bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨઢ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1l1l1lll_opy_ in bstack1l1llll1l_opy_.items():
    if isinstance(bstack1l1l1lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1l1lll_opy_:
          if idx<len(sys.argv) and bstack1l_opy_ (u"ࠧ࠮࠯ࠪણ") + var.lower() == val.lower() and not key in bstack1l1llll11_opy_:
            bstack1l1llll11_opy_[key] = sys.argv[idx+1]
            bstack1l1l11ll_opy_ += bstack1l_opy_ (u"ࠨࠢ࠰࠱ࠬત") + var + bstack1l_opy_ (u"ࠩࠣࠫથ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1l_opy_ (u"ࠪ࠱࠲࠭દ") + bstack1l1l1lll_opy_.lower() == val.lower() and not key in bstack1l1llll11_opy_:
          bstack1l1llll11_opy_[key] = sys.argv[idx+1]
          bstack1l1l11ll_opy_ += bstack1l_opy_ (u"ࠫࠥ࠳࠭ࠨધ") + bstack1l1l1lll_opy_ + bstack1l_opy_ (u"ࠬࠦࠧન") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1lll11l_opy_(config):
  bstack1l1llll1_opy_ = config.keys()
  for bstack11l111_opy_, bstack1l1l11l_opy_ in bstack11l1ll1ll_opy_.items():
    if bstack1l1l11l_opy_ in bstack1l1llll1_opy_:
      config[bstack11l111_opy_] = config[bstack1l1l11l_opy_]
      del config[bstack1l1l11l_opy_]
  for bstack11l111_opy_, bstack1l1l11l_opy_ in bstack1ll1111_opy_.items():
    if isinstance(bstack1l1l11l_opy_, list):
      for bstack11ll1l111_opy_ in bstack1l1l11l_opy_:
        if bstack11ll1l111_opy_ in bstack1l1llll1_opy_:
          config[bstack11l111_opy_] = config[bstack11ll1l111_opy_]
          del config[bstack11ll1l111_opy_]
          break
    elif bstack1l1l11l_opy_ in bstack1l1llll1_opy_:
        config[bstack11l111_opy_] = config[bstack1l1l11l_opy_]
        del config[bstack1l1l11l_opy_]
  for bstack11ll1l111_opy_ in list(config):
    for bstack11llllll1_opy_ in bstack1l1l11_opy_:
      if bstack11ll1l111_opy_.lower() == bstack11llllll1_opy_.lower() and bstack11ll1l111_opy_ != bstack11llllll1_opy_:
        config[bstack11llllll1_opy_] = config[bstack11ll1l111_opy_]
        del config[bstack11ll1l111_opy_]
  bstack11l1lll1_opy_ = []
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ઩") in config:
    bstack11l1lll1_opy_ = config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪપ")]
  for platform in bstack11l1lll1_opy_:
    for bstack11ll1l111_opy_ in list(platform):
      for bstack11llllll1_opy_ in bstack1l1l11_opy_:
        if bstack11ll1l111_opy_.lower() == bstack11llllll1_opy_.lower() and bstack11ll1l111_opy_ != bstack11llllll1_opy_:
          platform[bstack11llllll1_opy_] = platform[bstack11ll1l111_opy_]
          del platform[bstack11ll1l111_opy_]
  for bstack11l111_opy_, bstack1l1l11l_opy_ in bstack1ll1111_opy_.items():
    for platform in bstack11l1lll1_opy_:
      if isinstance(bstack1l1l11l_opy_, list):
        for bstack11ll1l111_opy_ in bstack1l1l11l_opy_:
          if bstack11ll1l111_opy_ in platform:
            platform[bstack11l111_opy_] = platform[bstack11ll1l111_opy_]
            del platform[bstack11ll1l111_opy_]
            break
      elif bstack1l1l11l_opy_ in platform:
        platform[bstack11l111_opy_] = platform[bstack1l1l11l_opy_]
        del platform[bstack1l1l11l_opy_]
  for bstack1lll111_opy_ in bstack11l11l_opy_:
    if bstack1lll111_opy_ in config:
      if not bstack11l11l_opy_[bstack1lll111_opy_] in config:
        config[bstack11l11l_opy_[bstack1lll111_opy_]] = {}
      config[bstack11l11l_opy_[bstack1lll111_opy_]].update(config[bstack1lll111_opy_])
      del config[bstack1lll111_opy_]
  for platform in bstack11l1lll1_opy_:
    for bstack1lll111_opy_ in bstack11l11l_opy_:
      if bstack1lll111_opy_ in list(platform):
        if not bstack11l11l_opy_[bstack1lll111_opy_] in platform:
          platform[bstack11l11l_opy_[bstack1lll111_opy_]] = {}
        platform[bstack11l11l_opy_[bstack1lll111_opy_]].update(platform[bstack1lll111_opy_])
        del platform[bstack1lll111_opy_]
  config = bstack11111l1_opy_(config)
  return config
def bstack1l1ll1111_opy_(config):
  global bstack1ll11l11l_opy_
  if bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬફ") in config and str(config[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭બ")]).lower() != bstack1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩભ"):
    if not bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨમ") in config:
      config[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩય")] = {}
    if not bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨર") in config[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")]:
      bstack11lll11l1_opy_ = datetime.datetime.now()
      bstack1lll11ll_opy_ = bstack11lll11l1_opy_.strftime(bstack1l_opy_ (u"ࠨࠧࡧࡣࠪࡨ࡟ࠦࡊࠨࡑࠬલ"))
      hostname = socket.gethostname()
      bstack1111ll_opy_ = bstack1l_opy_ (u"ࠩࠪળ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l_opy_ (u"ࠪࡿࢂࡥࡻࡾࡡࡾࢁࠬ઴").format(bstack1lll11ll_opy_, hostname, bstack1111ll_opy_)
      config[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨવ")][bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧશ")] = identifier
    bstack1ll11l11l_opy_ = config[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪષ")][bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩસ")]
  return config
def bstack1111lll1_opy_():
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
    return 0 # bstack1lllll_opy_ bstack11111ll1_opy_ not set build number env
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
def bstack1llllll1l_opy_(bstack11ll1l1ll_opy_):
  global CONFIG
  if not bstack1l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭૦") in CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૧")]:
    return
  CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")] = CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")].replace(
    bstack1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૪"),
    str(bstack11ll1l1ll_opy_)
  )
def bstack1ll1l11l1_opy_():
  global CONFIG
  if not bstack1l_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ૫") in CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૬")]:
    return
  bstack11lll11l1_opy_ = datetime.datetime.now()
  bstack1lll11ll_opy_ = bstack11lll11l1_opy_.strftime(bstack1l_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ૭"))
  CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")] = CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")].replace(
    bstack1l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭૰"),
    bstack1lll11ll_opy_
  )
def bstack11llll1_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱") in CONFIG and not bool(CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૲")]):
    del CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૳")]
    return
  if not bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴") in CONFIG:
    CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૵")] = bstack1l_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩ૶")
  if bstack1l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭૷") in CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૸")]:
    bstack1ll1l11l1_opy_()
    os.environ[bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ૹ")] = CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬૺ")]
  if not bstack1l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ૻ") in CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૼ")]:
    return
  bstack11ll1l1ll_opy_ = bstack1l_opy_ (u"࠭ࠧ૽")
  bstack1l11ll11l_opy_ = bstack1111lll1_opy_()
  if bstack1l11ll11l_opy_ != -1:
    bstack11ll1l1ll_opy_ = bstack1l_opy_ (u"ࠧࡄࡋࠣࠫ૾") + str(bstack1l11ll11l_opy_)
  if bstack11ll1l1ll_opy_ == bstack1l_opy_ (u"ࠨࠩ૿"):
    bstack1lllll111_opy_ = bstack11l1l1lll_opy_(CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ଀")])
    if bstack1lllll111_opy_ != -1:
      bstack11ll1l1ll_opy_ = str(bstack1lllll111_opy_)
  if bstack11ll1l1ll_opy_:
    bstack1llllll1l_opy_(bstack11ll1l1ll_opy_)
    os.environ[bstack1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧଁ")] = CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ଂ")]
def bstack11l1l111_opy_(bstack11ll1ll_opy_, bstack1ll11l_opy_, path):
  bstack1l11l11l1_opy_ = {
    bstack1l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩଃ"): bstack1ll11l_opy_
  }
  if os.path.exists(path):
    bstack1lll111l1_opy_ = json.load(open(path, bstack1l_opy_ (u"࠭ࡲࡣࠩ଄")))
  else:
    bstack1lll111l1_opy_ = {}
  bstack1lll111l1_opy_[bstack11ll1ll_opy_] = bstack1l11l11l1_opy_
  with open(path, bstack1l_opy_ (u"ࠢࡸ࠭ࠥଅ")) as outfile:
    json.dump(bstack1lll111l1_opy_, outfile)
def bstack11l1l1lll_opy_(bstack11ll1ll_opy_):
  bstack11ll1ll_opy_ = str(bstack11ll1ll_opy_)
  bstack1llll1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪଆ")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩଇ"))
  try:
    if not os.path.exists(bstack1llll1_opy_):
      os.makedirs(bstack1llll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬଈ")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଉ"), bstack1l_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧଊ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l_opy_ (u"࠭ࡷࠨଋ")):
        pass
      with open(file_path, bstack1l_opy_ (u"ࠢࡸ࠭ࠥଌ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l_opy_ (u"ࠨࡴࠪ଍")) as bstack1l11111l1_opy_:
      bstack1ll111_opy_ = json.load(bstack1l11111l1_opy_)
    if bstack11ll1ll_opy_ in bstack1ll111_opy_:
      bstack111lllll_opy_ = bstack1ll111_opy_[bstack11ll1ll_opy_][bstack1l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭଎")]
      bstack1111l_opy_ = int(bstack111lllll_opy_) + 1
      bstack11l1l111_opy_(bstack11ll1ll_opy_, bstack1111l_opy_, file_path)
      return bstack1111l_opy_
    else:
      bstack11l1l111_opy_(bstack11ll1ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11111_opy_.format(str(e)))
    return -1
def bstack1l11ll1l1_opy_(config):
  if not config[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬଏ")] or not config[bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧଐ")]:
    return True
  else:
    return False
def bstack11lllll1l_opy_(config):
  if bstack1l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ଑") in config:
    del(config[bstack1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ଒")])
    return False
  if bstack1ll11ll1_opy_() < version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭ଓ")):
    return False
  if bstack1ll11ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧଔ")):
    return True
  if bstack1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩକ") in config and config[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଖ")] == False:
    return False
  else:
    return True
def bstack1l1ll11ll_opy_(config, index = 0):
  global bstack1lll11l1_opy_
  bstack1ll1ll11_opy_ = {}
  caps = bstack11l1ll1l1_opy_ + bstack1ll1l11l_opy_
  if bstack1lll11l1_opy_:
    caps += bstack11l11ll1_opy_
  for key in config:
    if key in caps + [bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ")]:
      continue
    bstack1ll1ll11_opy_[key] = config[key]
  if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଘ") in config:
    for bstack1lll1ll_opy_ in config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଙ")][index]:
      if bstack1lll1ll_opy_ in caps + [bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଚ"), bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଛ")]:
        continue
      bstack1ll1ll11_opy_[bstack1lll1ll_opy_] = config[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ")][index][bstack1lll1ll_opy_]
  bstack1ll1ll11_opy_[bstack1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬଝ")] = socket.gethostname()
  if bstack1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬଞ") in bstack1ll1ll11_opy_:
    del(bstack1ll1ll11_opy_[bstack1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ଟ")])
  return bstack1ll1ll11_opy_
def bstack1lllll1_opy_(config):
  global bstack1lll11l1_opy_
  bstack1ll111ll1_opy_ = {}
  caps = bstack1ll1l11l_opy_
  if bstack1lll11l1_opy_:
    caps+= bstack11l11ll1_opy_
  for key in caps:
    if key in config:
      bstack1ll111ll1_opy_[key] = config[key]
  return bstack1ll111ll1_opy_
def bstack1l1l1llll_opy_(bstack1ll1ll11_opy_, bstack1ll111ll1_opy_):
  bstack1l11l1l1_opy_ = {}
  for key in bstack1ll1ll11_opy_.keys():
    if key in bstack11l1ll1ll_opy_:
      bstack1l11l1l1_opy_[bstack11l1ll1ll_opy_[key]] = bstack1ll1ll11_opy_[key]
    else:
      bstack1l11l1l1_opy_[key] = bstack1ll1ll11_opy_[key]
  for key in bstack1ll111ll1_opy_:
    if key in bstack11l1ll1ll_opy_:
      bstack1l11l1l1_opy_[bstack11l1ll1ll_opy_[key]] = bstack1ll111ll1_opy_[key]
    else:
      bstack1l11l1l1_opy_[key] = bstack1ll111ll1_opy_[key]
  return bstack1l11l1l1_opy_
def bstack1lll1111_opy_(config, index = 0):
  global bstack1lll11l1_opy_
  caps = {}
  bstack1ll111ll1_opy_ = bstack1lllll1_opy_(config)
  bstack111l111l_opy_ = bstack1ll1l11l_opy_
  bstack111l111l_opy_ += bstack11l1lll11_opy_
  if bstack1lll11l1_opy_:
    bstack111l111l_opy_ += bstack11l11ll1_opy_
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ") in config:
    if bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଡ") in config[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଢ")][index]:
      caps[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଣ")] = config[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ")][index][bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଥ")]
    if bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଦ") in config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index]:
      caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨନ")] = str(config[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪପ")])
    bstack1l1111l11_opy_ = {}
    for bstack11lll1ll_opy_ in bstack111l111l_opy_:
      if bstack11lll1ll_opy_ in config[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index]:
        if bstack11lll1ll_opy_ == bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ବ"):
          bstack1l1111l11_opy_[bstack11lll1ll_opy_] = str(config[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଭ")][index][bstack11lll1ll_opy_] * 1.0)
        else:
          bstack1l1111l11_opy_[bstack11lll1ll_opy_] = config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩମ")][index][bstack11lll1ll_opy_]
        del(config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଯ")][index][bstack11lll1ll_opy_])
    bstack1ll111ll1_opy_ = update(bstack1ll111ll1_opy_, bstack1l1111l11_opy_)
  bstack1ll1ll11_opy_ = bstack1l1ll11ll_opy_(config, index)
  for bstack11ll1l111_opy_ in bstack1ll1l11l_opy_ + [bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ର"), bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ଱")]:
    if bstack11ll1l111_opy_ in bstack1ll1ll11_opy_:
      bstack1ll111ll1_opy_[bstack11ll1l111_opy_] = bstack1ll1ll11_opy_[bstack11ll1l111_opy_]
      del(bstack1ll1ll11_opy_[bstack11ll1l111_opy_])
  if bstack11lllll1l_opy_(config):
    bstack1ll1ll11_opy_[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଲ")] = True
    caps.update(bstack1ll111ll1_opy_)
    caps[bstack1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬଳ")] = bstack1ll1ll11_opy_
  else:
    bstack1ll1ll11_opy_[bstack1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଴")] = False
    caps.update(bstack1l1l1llll_opy_(bstack1ll1ll11_opy_, bstack1ll111ll1_opy_))
    if bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଵ") in caps:
      caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨଶ")] = caps[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଷ")]
      del(caps[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧସ")])
    if bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫହ") in caps:
      caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭଺")] = caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭଻")]
      del(caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ଼ࠧ")])
  return caps
def bstack1l1l11ll1_opy_():
  global bstack1l1ll1ll1_opy_
  if bstack1ll11ll1_opy_() <= version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧଽ")):
    if bstack1l1ll1ll1_opy_ != bstack1l_opy_ (u"ࠨࠩା"):
      return bstack1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥି") + bstack1l1ll1ll1_opy_ + bstack1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢୀ")
    return bstack11ll1ll11_opy_
  if  bstack1l1ll1ll1_opy_ != bstack1l_opy_ (u"ࠫࠬୁ"):
    return bstack1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢୂ") + bstack1l1ll1ll1_opy_ + bstack1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢୃ")
  return bstack1l11_opy_
def bstack1l1ll1_opy_(options):
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
def bstack1ll1l1l1l_opy_(options, bstack1l1111_opy_):
  for bstack11ll1lll_opy_ in bstack1l1111_opy_:
    if bstack11ll1lll_opy_ in [bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୅"), bstack1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆")]:
      next
    if bstack11ll1lll_opy_ in options._experimental_options:
      options._experimental_options[bstack11ll1lll_opy_]= update(options._experimental_options[bstack11ll1lll_opy_], bstack1l1111_opy_[bstack11ll1lll_opy_])
    else:
      options.add_experimental_option(bstack11ll1lll_opy_, bstack1l1111_opy_[bstack11ll1lll_opy_])
  if bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨେ") in bstack1l1111_opy_:
    for arg in bstack1l1111_opy_[bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩୈ")]:
      options.add_argument(arg)
    del(bstack1l1111_opy_[bstack1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ୉")])
  if bstack1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ୊") in bstack1l1111_opy_:
    for ext in bstack1l1111_opy_[bstack1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫୋ")]:
      options.add_extension(ext)
    del(bstack1l1111_opy_[bstack1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬୌ")])
def bstack11ll111ll_opy_(options, bstack1ll1l111l_opy_):
  if bstack1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ୍") in bstack1ll1l111l_opy_:
    for bstack1l1ll1l1l_opy_ in bstack1ll1l111l_opy_[bstack1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ୎")]:
      if bstack1l1ll1l1l_opy_ in options._preferences:
        options._preferences[bstack1l1ll1l1l_opy_] = update(options._preferences[bstack1l1ll1l1l_opy_], bstack1ll1l111l_opy_[bstack1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ୏")][bstack1l1ll1l1l_opy_])
      else:
        options.set_preference(bstack1l1ll1l1l_opy_, bstack1ll1l111l_opy_[bstack1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୐")][bstack1l1ll1l1l_opy_])
  if bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ୑") in bstack1ll1l111l_opy_:
    for arg in bstack1ll1l111l_opy_[bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      options.add_argument(arg)
def bstack1l11l1111_opy_(options, bstack11llll1l1_opy_):
  if bstack1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩ୓") in bstack11llll1l1_opy_:
    options.use_webview(bool(bstack11llll1l1_opy_[bstack1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ୔")]))
  bstack1ll1l1l1l_opy_(options, bstack11llll1l1_opy_)
def bstack111111ll_opy_(options, bstack11ll1l1l_opy_):
  for bstack1l11l11_opy_ in bstack11ll1l1l_opy_:
    if bstack1l11l11_opy_ in [bstack1l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ୕"), bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩୖ")]:
      next
    options.set_capability(bstack1l11l11_opy_, bstack11ll1l1l_opy_[bstack1l11l11_opy_])
  if bstack1l_opy_ (u"ࠬࡧࡲࡨࡵࠪୗ") in bstack11ll1l1l_opy_:
    for arg in bstack11ll1l1l_opy_[bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ୘")]:
      options.add_argument(arg)
  if bstack1l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ୙") in bstack11ll1l1l_opy_:
    options.use_technology_preview(bool(bstack11ll1l1l_opy_[bstack1l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬ୚")]))
def bstack11llll1ll_opy_(options, bstack1ll1l1l_opy_):
  for bstack1l1l11l1_opy_ in bstack1ll1l1l_opy_:
    if bstack1l1l11l1_opy_ in [bstack1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୛"), bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଡ଼")]:
      next
    options._options[bstack1l1l11l1_opy_] = bstack1ll1l1l_opy_[bstack1l1l11l1_opy_]
  if bstack1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨଢ଼") in bstack1ll1l1l_opy_:
    for bstack1l1lll11l_opy_ in bstack1ll1l1l_opy_[bstack1l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୞")]:
      options.add_additional_option(
          bstack1l1lll11l_opy_, bstack1ll1l1l_opy_[bstack1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪୟ")][bstack1l1lll11l_opy_])
  if bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬୠ") in bstack1ll1l1l_opy_:
    for arg in bstack1ll1l1l_opy_[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ୡ")]:
      options.add_argument(arg)
def bstack1llll11l1_opy_(options, caps):
  if not hasattr(options, bstack1l_opy_ (u"ࠩࡎࡉ࡞࠭ୢ")):
    return
  if options.KEY == bstack1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨୣ") and options.KEY in caps:
    bstack1ll1l1l1l_opy_(options, caps[bstack1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୤")])
  elif options.KEY == bstack1l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ୥") and options.KEY in caps:
    bstack11ll111ll_opy_(options, caps[bstack1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ୦")])
  elif options.KEY == bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ୧") and options.KEY in caps:
    bstack111111ll_opy_(options, caps[bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ୨")])
  elif options.KEY == bstack1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୩") and options.KEY in caps:
    bstack1l11l1111_opy_(options, caps[bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ୪")])
  elif options.KEY == bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୫") and options.KEY in caps:
    bstack11llll1ll_opy_(options, caps[bstack1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୬")])
def bstack1111l11_opy_(caps):
  global bstack1lll11l1_opy_
  if bstack1lll11l1_opy_:
    if bstack111l1l11_opy_() < version.parse(bstack1l_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬ୭")):
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
      if not bstack1l1ll1_opy_(options):
        return None
      for bstack11ll1l111_opy_ in caps.keys():
        options.set_capability(bstack11ll1l111_opy_, caps[bstack11ll1l111_opy_])
      bstack1llll11l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l11ll1l_opy_(options, bstack1ll11l1l_opy_):
  if not bstack1l1ll1_opy_(options):
    return
  for bstack11ll1l111_opy_ in bstack1ll11l1l_opy_.keys():
    if bstack11ll1l111_opy_ in bstack11l1lll11_opy_:
      next
    if bstack11ll1l111_opy_ in options._caps and type(options._caps[bstack11ll1l111_opy_]) in [dict, list]:
      options._caps[bstack11ll1l111_opy_] = update(options._caps[bstack11ll1l111_opy_], bstack1ll11l1l_opy_[bstack11ll1l111_opy_])
    else:
      options.set_capability(bstack11ll1l111_opy_, bstack1ll11l1l_opy_[bstack11ll1l111_opy_])
  bstack1llll11l1_opy_(options, bstack1ll11l1l_opy_)
  if bstack1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ୿") in options._caps:
    if options._caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ஀")] and options._caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ஁")].lower() != bstack1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧஂ"):
      del options._caps[bstack1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ஃ")]
def bstack1111ll1_opy_(proxy_config):
  if bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ஄") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫஅ")] = proxy_config[bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧஆ")]
    del(proxy_config[bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨஇ")])
  if bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨஈ") in proxy_config and proxy_config[bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஉ")].lower() != bstack1l_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧஊ"):
    proxy_config[bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஋")] = bstack1l_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩ஌")
  if bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨ஍") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧஎ")] = bstack1l_opy_ (u"ࠬࡶࡡࡤࠩஏ")
  return proxy_config
def bstack1lll1ll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬஐ") in config:
    return proxy
  config[bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭஑")] = bstack1111ll1_opy_(config[bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧஒ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨஓ")])
  return proxy
def bstack11l1l1l1_opy_(self):
  global CONFIG
  global bstack1ll1l1ll_opy_
  if bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ") in CONFIG:
    return CONFIG[bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧக")]
  elif bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஖") in CONFIG:
    return CONFIG[bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ஗")]
  else:
    return bstack1ll1l1ll_opy_(self)
def bstack111l11ll_opy_():
  global CONFIG
  return bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ஘") in CONFIG or bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬங") in CONFIG
def bstack1ll11111l_opy_(config):
  if not bstack111l11ll_opy_():
    return
  if config.get(bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬச")):
    return config.get(bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭஛"))
  if config.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨஜ")):
    return config.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஝"))
def bstack1l1lll1l1_opy_():
  return bstack111l11ll_opy_() and bstack1ll11ll1_opy_() >= version.parse(bstack11ll1111_opy_)
def bstack11lll11l_opy_(config):
  if bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪஞ") in config:
    return config[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫட")]
  if bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ஠") in config:
    return config[bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ஡")]
  return {}
def bstack1ll1lll11_opy_(config):
  if bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ஢") in config:
    return config[bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩண")]
  return {}
def bstack11ll1llll_opy_(caps):
  global bstack1ll11l11l_opy_
  if bstack1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭த") in caps:
    caps[bstack1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ஥")][bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭஦")] = True
    if bstack1ll11l11l_opy_:
      caps[bstack1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ஧")][bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫந")] = bstack1ll11l11l_opy_
  else:
    caps[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨன")] = True
    if bstack1ll11l11l_opy_:
      caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬப")] = bstack1ll11l11l_opy_
def bstack1l1lll1l_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ஫") in CONFIG and CONFIG[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ஬")]:
    bstack1111111l_opy_ = bstack11lll11l_opy_(CONFIG)
    bstack1lll1l1l1_opy_(CONFIG[bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ஭")], bstack1111111l_opy_)
def bstack1lll1l1l1_opy_(key, bstack1111111l_opy_):
  global bstack1l11l_opy_
  logger.info(bstack11l11l1l_opy_)
  try:
    bstack1l11l_opy_ = Local()
    bstack1l1l1_opy_ = {bstack1l_opy_ (u"ࠨ࡭ࡨࡽࠬம"): key}
    bstack1l1l1_opy_.update(bstack1111111l_opy_)
    logger.debug(bstack1llll1ll_opy_.format(str(bstack1l1l1_opy_)))
    bstack1l11l_opy_.start(**bstack1l1l1_opy_)
    if bstack1l11l_opy_.isRunning():
      logger.info(bstack11llll11l_opy_)
  except Exception as e:
    bstack1l11l1lll_opy_(bstack1lll1l1ll_opy_.format(str(e)))
def bstack1lll1lll1_opy_():
  global bstack1l11l_opy_
  if bstack1l11l_opy_.isRunning():
    logger.info(bstack11l1111_opy_)
    bstack1l11l_opy_.stop()
  bstack1l11l_opy_ = None
def bstack1ll1l111_opy_():
  global bstack1l1l1111l_opy_
  global bstack11ll_opy_
  if bstack1l1l1111l_opy_:
    logger.warning(bstack1l1l1ll1l_opy_.format(str(bstack1l1l1111l_opy_)))
  logger.info(bstack1ll11llll_opy_)
  global bstack1l11l_opy_
  if bstack1l11l_opy_:
    bstack1lll1lll1_opy_()
  try:
    for driver in bstack11ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l11111_opy_)
  bstack1l11l11l_opy_()
def bstack1l111llll_opy_(self, *args):
  logger.error(bstack1l11l1l11_opy_)
  bstack1ll1l111_opy_()
  sys.exit(1)
def bstack1l11l1lll_opy_(err):
  logger.critical(bstack11l1ll11_opy_.format(str(err)))
  bstack1l11l11l_opy_(bstack11l1ll11_opy_.format(str(err)))
  atexit.unregister(bstack1ll1l111_opy_)
  sys.exit(1)
def bstack1l111l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l11l11l_opy_(message)
  atexit.unregister(bstack1ll1l111_opy_)
  sys.exit(1)
def bstack1lllll1l_opy_():
  global CONFIG
  global bstack1l1llll11_opy_
  global bstack1l111l1l_opy_
  global bstack1l111l11l_opy_
  CONFIG = bstack1l11ll_opy_()
  bstack1l11lll_opy_()
  bstack11ll1l_opy_()
  CONFIG = bstack1lll11l_opy_(CONFIG)
  update(CONFIG, bstack1l111l1l_opy_)
  update(CONFIG, bstack1l1llll11_opy_)
  CONFIG = bstack1l1ll1111_opy_(CONFIG)
  if bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ய") in CONFIG and str(CONFIG[bstack1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧர")]).lower() == bstack1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪற"):
    bstack1l111l11l_opy_ = False
  if (bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨல") in CONFIG and bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩள") in bstack1l1llll11_opy_) or (bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪழ") in CONFIG and bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫவ") not in bstack1l111l1l_opy_):
    if os.getenv(bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ஶ")):
      CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬஷ")] = os.getenv(bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨஸ"))
    else:
      bstack11llll1_opy_()
  elif (bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨஹ") not in CONFIG and bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ஺") in CONFIG) or (bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஻") in bstack1l111l1l_opy_ and bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ஼") not in bstack1l1llll11_opy_):
    del(CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ஽")])
  if bstack1l11ll1l1_opy_(CONFIG):
    bstack1l11l1lll_opy_(bstack11l11111_opy_)
  bstack1l1l1l1_opy_()
  bstack11l1ll1_opy_()
  if bstack1lll11l1_opy_:
    CONFIG[bstack1l_opy_ (u"ࠪࡥࡵࡶࠧா")] = bstack1lll1l1_opy_(CONFIG)
    logger.info(bstack111lll11_opy_.format(CONFIG[bstack1l_opy_ (u"ࠫࡦࡶࡰࠨி")]))
def bstack11l1ll1_opy_():
  global CONFIG
  global bstack1lll11l1_opy_
  if bstack1l_opy_ (u"ࠬࡧࡰࡱࠩீ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l111l1_opy_(e, bstack1l11lll11_opy_)
    bstack1lll11l1_opy_ = True
def bstack1lll1l1_opy_(config):
  bstack1l11llll1_opy_ = bstack1l_opy_ (u"࠭ࠧு")
  app = config[bstack1l_opy_ (u"ࠧࡢࡲࡳࠫூ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11l1ll_opy_:
      if os.path.exists(app):
        bstack1l11llll1_opy_ = bstack11l11lll_opy_(config, app)
      elif bstack11l1lllll_opy_(app):
        bstack1l11llll1_opy_ = app
      else:
        bstack1l11l1lll_opy_(bstack1l11lll1_opy_.format(app))
    else:
      if bstack11l1lllll_opy_(app):
        bstack1l11llll1_opy_ = app
      elif os.path.exists(app):
        bstack1l11llll1_opy_ = bstack11l11lll_opy_(app)
      else:
        bstack1l11l1lll_opy_(bstack1l1l1ll11_opy_)
  else:
    if len(app) > 2:
      bstack1l11l1lll_opy_(bstack1ll111l1_opy_)
    elif len(app) == 2:
      if bstack1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭௃") in app and bstack1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ௄") in app:
        if os.path.exists(app[bstack1l_opy_ (u"ࠪࡴࡦࡺࡨࠨ௅")]):
          bstack1l11llll1_opy_ = bstack11l11lll_opy_(config, app[bstack1l_opy_ (u"ࠫࡵࡧࡴࡩࠩெ")], app[bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨே")])
        else:
          bstack1l11l1lll_opy_(bstack1l11lll1_opy_.format(app))
      else:
        bstack1l11l1lll_opy_(bstack1ll111l1_opy_)
    else:
      for key in app:
        if key in bstack1lll1ll11_opy_:
          if key == bstack1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫை"):
            if os.path.exists(app[key]):
              bstack1l11llll1_opy_ = bstack11l11lll_opy_(config, app[key])
            else:
              bstack1l11l1lll_opy_(bstack1l11lll1_opy_.format(app))
          else:
            bstack1l11llll1_opy_ = app[key]
        else:
          bstack1l11l1lll_opy_(bstack1ll11_opy_)
  return bstack1l11llll1_opy_
def bstack11l1lllll_opy_(bstack1l11llll1_opy_):
  import re
  bstack1llll11_opy_ = re.compile(bstack1l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ௉"))
  bstack11lll1ll1_opy_ = re.compile(bstack1l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧொ"))
  if bstack1l_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨோ") in bstack1l11llll1_opy_ or re.fullmatch(bstack1llll11_opy_, bstack1l11llll1_opy_) or re.fullmatch(bstack11lll1ll1_opy_, bstack1l11llll1_opy_):
    return True
  else:
    return False
def bstack11l11lll_opy_(config, path, bstack1l1ll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l_opy_ (u"ࠪࡶࡧ࠭ௌ")).read()).hexdigest()
  bstack1lllll11_opy_ = bstack11l1lll1l_opy_(md5_hash)
  bstack1l11llll1_opy_ = None
  if bstack1lllll11_opy_:
    logger.info(bstack1llll1ll1_opy_.format(bstack1lllll11_opy_, md5_hash))
    return bstack1lllll11_opy_
  bstack111l1l_opy_ = MultipartEncoder(
    fields={
        bstack1l_opy_ (u"ࠫ࡫࡯࡬ࡦ்ࠩ"): (os.path.basename(path), open(os.path.abspath(path), bstack1l_opy_ (u"ࠬࡸࡢࠨ௎")), bstack1l_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ௏")),
        bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪௐ"): bstack1l1ll1l_opy_
    }
  )
  response = requests.post(bstack1lllllll1_opy_, data=bstack111l1l_opy_,
                         headers={bstack1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ௑"): bstack111l1l_opy_.content_type}, auth=(config[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ௒")], config[bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭௓")]))
  try:
    res = json.loads(response.text)
    bstack1l11llll1_opy_ = res[bstack1l_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ௔")]
    logger.info(bstack11llll1l_opy_.format(bstack1l11llll1_opy_))
    bstack11l11l11_opy_(md5_hash, bstack1l11llll1_opy_)
  except ValueError as err:
    bstack1l11l1lll_opy_(bstack1ll1l1_opy_.format(str(err)))
  return bstack1l11llll1_opy_
def bstack1l1l1l1_opy_():
  global CONFIG
  global bstack11l1ll11l_opy_
  bstack11l1l11ll_opy_ = 0
  bstack1lll11l11_opy_ = 1
  if bstack1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ௕") in CONFIG:
    bstack1lll11l11_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭௖")]
  if bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪௗ") in CONFIG:
    bstack11l1l11ll_opy_ = len(CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௘")])
  bstack11l1ll11l_opy_ = int(bstack1lll11l11_opy_) * int(bstack11l1l11ll_opy_)
def bstack11l1lll1l_opy_(md5_hash):
  bstack1111l11l_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠩࢁࠫ௙")), bstack1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ௚"), bstack1l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ௛"))
  if os.path.exists(bstack1111l11l_opy_):
    bstack1l1llllll_opy_ = json.load(open(bstack1111l11l_opy_,bstack1l_opy_ (u"ࠬࡸࡢࠨ௜")))
    if md5_hash in bstack1l1llllll_opy_:
      bstack11ll11l1_opy_ = bstack1l1llllll_opy_[md5_hash]
      bstack11lll1lll_opy_ = datetime.datetime.now()
      bstack1llll1lll_opy_ = datetime.datetime.strptime(bstack11ll11l1_opy_[bstack1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ௝")], bstack1l_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫ௞"))
      if (bstack11lll1lll_opy_ - bstack1llll1lll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11ll11l1_opy_[bstack1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭௟")]):
        return None
      return bstack11ll11l1_opy_[bstack1l_opy_ (u"ࠩ࡬ࡨࠬ௠")]
  else:
    return None
def bstack11l11l11_opy_(md5_hash, bstack1l11llll1_opy_):
  bstack1llll1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬ௡")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ௢"))
  if not os.path.exists(bstack1llll1_opy_):
    os.makedirs(bstack1llll1_opy_)
  bstack1111l11l_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠬࢄࠧ௣")), bstack1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭௤"), bstack1l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ௥"))
  bstack1lll11111_opy_ = {
    bstack1l_opy_ (u"ࠨ࡫ࡧࠫ௦"): bstack1l11llll1_opy_,
    bstack1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ௧"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ௨")),
    bstack1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ௩"): str(__version__)
  }
  if os.path.exists(bstack1111l11l_opy_):
    bstack1l1llllll_opy_ = json.load(open(bstack1111l11l_opy_,bstack1l_opy_ (u"ࠬࡸࡢࠨ௪")))
  else:
    bstack1l1llllll_opy_ = {}
  bstack1l1llllll_opy_[md5_hash] = bstack1lll11111_opy_
  with open(bstack1111l11l_opy_, bstack1l_opy_ (u"ࠨࡷࠬࠤ௫")) as outfile:
    json.dump(bstack1l1llllll_opy_, outfile)
def bstack111111l_opy_(self):
  return
def bstack111ll111_opy_(self):
  return
def bstack111l11l_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1llllllll_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack111ll1_opy_
  global bstack1l1111ll1_opy_
  global bstack1l1l111l1_opy_
  global bstack11ll1l11l_opy_
  global bstack11l1ll111_opy_
  global bstack1ll111lll_opy_
  global bstack11ll_opy_
  global bstack1llllll11_opy_
  CONFIG[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ௬")] = str(bstack11l1ll111_opy_) + str(__version__)
  command_executor = bstack1l1l11ll1_opy_()
  logger.debug(bstack11l1111l_opy_.format(command_executor))
  proxy = bstack1lll1ll1l_opy_(CONFIG, proxy)
  bstack11ll1l11_opy_ = 0 if bstack1l1111ll1_opy_ < 0 else bstack1l1111ll1_opy_
  if bstack11ll1l11l_opy_ is True:
    bstack11ll1l11_opy_ = int(threading.current_thread().getName())
  bstack1ll11l1l_opy_ = bstack1lll1111_opy_(CONFIG, bstack11ll1l11_opy_)
  logger.debug(bstack1ll11ll_opy_.format(str(bstack1ll11l1l_opy_)))
  if bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ௭") in CONFIG and CONFIG[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭௮")]:
    bstack11ll1llll_opy_(bstack1ll11l1l_opy_)
  if desired_capabilities:
    bstack1ll11ll11_opy_ = bstack1lll11l_opy_(desired_capabilities)
    bstack1ll11ll11_opy_[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ௯")] = bstack11lllll1l_opy_(CONFIG)
    bstack1l1ll1l11_opy_ = bstack1lll1111_opy_(bstack1ll11ll11_opy_)
    if bstack1l1ll1l11_opy_:
      bstack1ll11l1l_opy_ = update(bstack1l1ll1l11_opy_, bstack1ll11l1l_opy_)
    desired_capabilities = None
  if options:
    bstack1l11ll1l_opy_(options, bstack1ll11l1l_opy_)
  if not options:
    options = bstack1111l11_opy_(bstack1ll11l1l_opy_)
  if proxy and bstack1ll11ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ௰")):
    options.proxy(proxy)
  if options and bstack1ll11ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ௱")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1ll11ll1_opy_() < version.parse(bstack1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ௲")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll11l1l_opy_)
  logger.info(bstack1l11l111l_opy_)
  if bstack1ll11ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ௳")):
    bstack1ll111lll_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll11ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ௴")):
    bstack1ll111lll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll11ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ௵")):
    bstack1ll111lll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1ll111lll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack11ll11lll_opy_ = bstack1l_opy_ (u"ࠪࠫ௶")
    if bstack1ll11ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ௷")):
      bstack11ll11lll_opy_ = self.caps.get(bstack1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ௸"))
    else:
      bstack11ll11lll_opy_ = self.capabilities.get(bstack1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ௹"))
    if bstack11ll11lll_opy_:
      if bstack1ll11ll1_opy_() <= version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ௺")):
        self.command_executor._url = bstack1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ௻") + bstack1l1ll1ll1_opy_ + bstack1l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ௼")
      else:
        self.command_executor._url = bstack1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ௽") + bstack11ll11lll_opy_ + bstack1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ௾")
      logger.debug(bstack1l111111l_opy_.format(bstack11ll11lll_opy_))
    else:
      logger.debug(bstack11l111ll_opy_.format(bstack1l_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ௿")))
  except Exception as e:
    logger.debug(bstack11l111ll_opy_.format(e))
  bstack11lll_opy_(bstack1l1111ll1_opy_, bstack1llllll11_opy_)
  bstack111ll1_opy_ = self.session_id
  bstack11ll_opy_.append(self)
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఀ") in CONFIG and bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఁ") in CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫం")][bstack11ll1l11_opy_]:
    bstack1l1l111l1_opy_ = CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬః")][bstack11ll1l11_opy_][bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨఄ")]
  logger.debug(bstack1l1111lll_opy_.format(bstack111ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l1l1111_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1l1l1l_opy_
      if(bstack1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺ࠱࡮ࡸࠨఅ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠬࢄࠧఆ")), bstack1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ఇ"), bstack1l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩఈ")), bstack1l_opy_ (u"ࠨࡹࠪఉ")) as fp:
          fp.write(bstack1l_opy_ (u"ࠤࠥఊ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧఋ")))):
          with open(args[1], bstack1l_opy_ (u"ࠫࡷ࠭ఌ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l_opy_ (u"ࠬࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦ࡟࡯ࡧࡺࡔࡦ࡭ࡥࠩࡥࡲࡲࡹ࡫ࡸࡵ࠮ࠣࡴࡦ࡭ࡥࠡ࠿ࠣࡺࡴ࡯ࡤࠡ࠲ࠬࠫ఍") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l11ll_opy_)
            lines.insert(1, bstack1ll11l111_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣఎ")), bstack1l_opy_ (u"ࠧࡸࠩఏ")) as bstack1l1l111ll_opy_:
              bstack1l1l111ll_opy_.writelines(lines)
        CONFIG[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪఐ")] = str(bstack11l1ll111_opy_) + str(__version__)
        bstack11ll1l11_opy_ = 0 if bstack1l1111ll1_opy_ < 0 else bstack1l1111ll1_opy_
        if bstack11ll1l11l_opy_ is True:
          bstack11ll1l11_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ఑")] = False
        CONFIG[bstack1l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤఒ")] = True
        bstack1ll11l1l_opy_ = bstack1lll1111_opy_(CONFIG, bstack11ll1l11_opy_)
        logger.debug(bstack1ll11ll_opy_.format(str(bstack1ll11l1l_opy_)))
        if CONFIG[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨఓ")]:
          bstack11ll1llll_opy_(bstack1ll11l1l_opy_)
        if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఔ") in CONFIG and bstack1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫక") in CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఖ")][bstack11ll1l11_opy_]:
          bstack1l1l111l1_opy_ = CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫగ")][bstack11ll1l11_opy_][bstack1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧఘ")]
        args.append(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬఙ")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫచ"), bstack1l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧఛ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll11l1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣజ"))
      bstack1l1l1l1l_opy_ = True
      return bstack1l1111l_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack11l11l1_opy_(self,
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
    global bstack111ll1_opy_
    global bstack1l1111ll1_opy_
    global bstack1l1l111l1_opy_
    global bstack11ll1l11l_opy_
    global bstack11l1ll111_opy_
    global bstack1ll111lll_opy_
    CONFIG[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩఝ")] = str(bstack11l1ll111_opy_) + str(__version__)
    bstack11ll1l11_opy_ = 0 if bstack1l1111ll1_opy_ < 0 else bstack1l1111ll1_opy_
    if bstack11ll1l11l_opy_ is True:
      bstack11ll1l11_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢఞ")] = True
    bstack1ll11l1l_opy_ = bstack1lll1111_opy_(CONFIG, bstack11ll1l11_opy_)
    logger.debug(bstack1ll11ll_opy_.format(str(bstack1ll11l1l_opy_)))
    if CONFIG[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ట")]:
      bstack11ll1llll_opy_(bstack1ll11l1l_opy_)
    if bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఠ") in CONFIG and bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩడ") in CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఢ")][bstack11ll1l11_opy_]:
      bstack1l1l111l1_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩణ")][bstack11ll1l11_opy_][bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬత")]
    import urllib
    import json
    bstack1lll1l111_opy_ = bstack1l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪథ") + urllib.parse.quote(json.dumps(bstack1ll11l1l_opy_))
    browser = self.connect(bstack1lll1l111_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1lll11_opy_():
    global bstack1l1l1l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l11l1_opy_
        bstack1l1l1l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1l1111_opy_
      bstack1l1l1l1l_opy_ = True
    except Exception as e:
      pass
def bstack11lll11ll_opy_(context, bstack1ll11l1_opy_):
  try:
    context.page.evaluate(bstack1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥద"), bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧధ")+ json.dumps(bstack1ll11l1_opy_) + bstack1l_opy_ (u"ࠦࢂࢃࠢన"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥ఩"), e)
def bstack1111_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢప"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬఫ") + json.dumps(message) + bstack1l_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫబ") + json.dumps(level) + bstack1l_opy_ (u"ࠩࢀࢁࠬభ"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨమ"), e)
def bstack11l1_opy_(context, status, message = bstack1l_opy_ (u"ࠦࠧయ")):
  try:
    if(status == bstack1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧర")):
      context.page.evaluate(bstack1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢఱ"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠨల") + json.dumps(bstack1l_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢࠥళ") + str(message)) + bstack1l_opy_ (u"ࠩ࠯ࠦࡸࡺࡡࡵࡷࡶࠦ࠿࠭ఴ") + json.dumps(status) + bstack1l_opy_ (u"ࠥࢁࢂࠨవ"))
    else:
      context.page.evaluate(bstack1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧశ"), bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿࠭ష") + json.dumps(status) + bstack1l_opy_ (u"ࠨࡽࡾࠤస"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦహ"), e)
def bstack1l1lll1ll_opy_(self, url):
  global bstack1ll1lllll_opy_
  try:
    bstack1lll1ll1_opy_(url)
  except Exception as err:
    logger.debug(bstack111ll1ll_opy_.format(str(err)))
  try:
    bstack1ll1lllll_opy_(self, url)
  except Exception as e:
    try:
      bstack1llll111_opy_ = str(e)
      if any(err_msg in bstack1llll111_opy_ for err_msg in bstack1ll1llll_opy_):
        bstack1lll1ll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111ll1ll_opy_.format(str(err)))
    raise e
def bstack1l1ll1lll_opy_(self):
  global bstack1l1111111_opy_
  bstack1l1111111_opy_ = self
  return
def bstack1l1l1ll1_opy_(self, test):
  global CONFIG
  global bstack1l1111111_opy_
  global bstack111ll1_opy_
  global bstack1llll_opy_
  global bstack1l1l111l1_opy_
  global bstack111lll1l_opy_
  global bstack1llll1111_opy_
  global bstack11ll_opy_
  try:
    if not bstack111ll1_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪ఺")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ఻"), bstack1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸ఼ࠬ"))) as f:
        bstack1l11l1ll1_opy_ = json.loads(bstack1l_opy_ (u"ࠦࢀࠨఽ") + f.read().strip() + bstack1l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧా") + bstack1l_opy_ (u"ࠨࡽࠣి"))
        bstack111ll1_opy_ = bstack1l11l1ll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11ll_opy_:
    for driver in bstack11ll_opy_:
      if bstack111ll1_opy_ == driver.session_id:
        if test:
          bstack1lll1l11_opy_ = str(test.data)
        if not bstack11llll_opy_ and bstack1lll1l11_opy_:
          bstack1ll11l1l1_opy_ = {
            bstack1l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧీ"): bstack1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩు"),
            bstack1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬూ"): {
              bstack1l_opy_ (u"ࠪࡲࡦࡳࡥࠨృ"): bstack1lll1l11_opy_
            }
          }
          bstack1l1ll_opy_ = bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩౄ").format(json.dumps(bstack1ll11l1l1_opy_))
          driver.execute_script(bstack1l1ll_opy_)
        if bstack1llll_opy_:
          bstack11ll11111_opy_ = {
            bstack1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ౅"): bstack1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨె"),
            bstack1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪే"): {
              bstack1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ై"): bstack1lll1l11_opy_ + bstack1l_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ౉"),
              bstack1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩొ"): bstack1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩో")
            }
          }
          bstack1ll11l1l1_opy_ = {
            bstack1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬౌ"): bstack1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴ్ࠩ"),
            bstack1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ౎"): {
              bstack1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ౏"): bstack1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౐")
            }
          }
          if bstack1llll_opy_.status == bstack1l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ౑"):
            bstack1l1ll11l1_opy_ = bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ౒").format(json.dumps(bstack11ll11111_opy_))
            driver.execute_script(bstack1l1ll11l1_opy_)
            bstack1l1ll_opy_ = bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ౓").format(json.dumps(bstack1ll11l1l1_opy_))
            driver.execute_script(bstack1l1ll_opy_)
          elif bstack1llll_opy_.status == bstack1l_opy_ (u"࠭ࡆࡂࡋࡏࠫ౔"):
            reason = bstack1l_opy_ (u"ౕࠢࠣ")
            bstack1llll111l_opy_ = bstack1lll1l11_opy_ + bstack1l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥౖࠩ")
            if bstack1llll_opy_.message:
              reason = str(bstack1llll_opy_.message)
              bstack1llll111l_opy_ = bstack1llll111l_opy_ + bstack1l_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩ౗") + reason
            bstack11ll11111_opy_[bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ౘ")] = {
              bstack1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪౙ"): bstack1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫౚ"),
              bstack1l_opy_ (u"࠭ࡤࡢࡶࡤࠫ౛"): bstack1llll111l_opy_
            }
            bstack1ll11l1l1_opy_[bstack1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ౜")] = {
              bstack1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨౝ"): bstack1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౞"),
              bstack1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ౟"): reason
            }
            bstack1l1ll11l1_opy_ = bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩౠ").format(json.dumps(bstack11ll11111_opy_))
            driver.execute_script(bstack1l1ll11l1_opy_)
            bstack1l1ll_opy_ = bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪౡ").format(json.dumps(bstack1ll11l1l1_opy_))
            driver.execute_script(bstack1l1ll_opy_)
  elif bstack111ll1_opy_:
    try:
      data = {}
      bstack1lll1l11_opy_ = None
      if test:
        bstack1lll1l11_opy_ = str(test.data)
      if not bstack11llll_opy_ and bstack1lll1l11_opy_:
        data[bstack1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫౢ")] = bstack1lll1l11_opy_
      if bstack1llll_opy_:
        if bstack1llll_opy_.status == bstack1l_opy_ (u"ࠧࡑࡃࡖࡗࠬౣ"):
          data[bstack1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ౤")] = bstack1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ౥")
        elif bstack1llll_opy_.status == bstack1l_opy_ (u"ࠪࡊࡆࡏࡌࠨ౦"):
          data[bstack1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ౧")] = bstack1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ౨")
          if bstack1llll_opy_.message:
            data[bstack1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭౩")] = str(bstack1llll_opy_.message)
      user = CONFIG[bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ౪")]
      key = CONFIG[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ౫")]
      url = bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧ౬").format(user, key, bstack111ll1_opy_)
      headers = {
        bstack1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ౭"): bstack1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ౮"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1111ll11_opy_.format(str(e)))
  if bstack1l1111111_opy_:
    bstack1llll1111_opy_(bstack1l1111111_opy_)
  bstack111lll1l_opy_(self, test)
def bstack111ll11l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l1lll_opy_
  bstack11l1lll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1llll_opy_
  bstack1llll_opy_ = self._test
def bstack11111l1l_opy_():
  global bstack11lllll_opy_
  if os.path.exists(bstack11lllll_opy_):
    os.remove(bstack11lllll_opy_)
def bstack1l1111l1_opy_():
  global bstack11lllll_opy_
  if not os.path.isfile(bstack11lllll_opy_):
    with open(bstack11lllll_opy_, bstack1l_opy_ (u"ࠬࡽࠧ౯")):
      pass
    with open(bstack11lllll_opy_, bstack1l_opy_ (u"ࠨࡷࠬࠤ౰")) as outfile:
      json.dump({}, outfile)
  bstack1lll111l1_opy_ = {}
  if os.path.exists(bstack11lllll_opy_):
    bstack1lll111l1_opy_ = json.load(open(bstack11lllll_opy_, bstack1l_opy_ (u"ࠧࡳࡤࠪ౱")))
  return bstack1lll111l1_opy_
def bstack11lll_opy_(platform_index, item_index):
  global bstack11lllll_opy_
  bstack1lll111l1_opy_ = bstack1l1111l1_opy_()
  bstack1lll111l1_opy_[item_index] = platform_index
  with open(bstack11lllll_opy_, bstack1l_opy_ (u"ࠣࡹ࠮ࠦ౲")) as outfile:
    json.dump(bstack1lll111l1_opy_, outfile)
def bstack1l1l11lll_opy_(bstack1lll111l_opy_):
  global CONFIG
  bstack1l111ll1_opy_ = bstack1l_opy_ (u"ࠩࠪ౳")
  if not bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౴") in CONFIG:
    logger.info(bstack1l_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ౵"))
  try:
    platform = CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౶")][bstack1lll111l_opy_]
    if bstack1l_opy_ (u"࠭࡯ࡴࠩ౷") in platform:
      bstack1l111ll1_opy_ += str(platform[bstack1l_opy_ (u"ࠧࡰࡵࠪ౸")]) + bstack1l_opy_ (u"ࠨ࠮ࠣࠫ౹")
    if bstack1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ౺") in platform:
      bstack1l111ll1_opy_ += str(platform[bstack1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౻")]) + bstack1l_opy_ (u"ࠫ࠱ࠦࠧ౼")
    if bstack1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ౽") in platform:
      bstack1l111ll1_opy_ += str(platform[bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ౾")]) + bstack1l_opy_ (u"ࠧ࠭ࠢࠪ౿")
    if bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪಀ") in platform:
      bstack1l111ll1_opy_ += str(platform[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫಁ")]) + bstack1l_opy_ (u"ࠪ࠰ࠥ࠭ಂ")
    if bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩಃ") in platform:
      bstack1l111ll1_opy_ += str(platform[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ಄")]) + bstack1l_opy_ (u"࠭ࠬࠡࠩಅ")
    if bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨಆ") in platform:
      bstack1l111ll1_opy_ += str(platform[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩಇ")]) + bstack1l_opy_ (u"ࠩ࠯ࠤࠬಈ")
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪಉ") + str(e))
  finally:
    if bstack1l111ll1_opy_[len(bstack1l111ll1_opy_) - 2:] == bstack1l_opy_ (u"ࠫ࠱ࠦࠧಊ"):
      bstack1l111ll1_opy_ = bstack1l111ll1_opy_[:-2]
    return bstack1l111ll1_opy_
def bstack1llll1l_opy_(path, bstack1l111ll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11l1l111l_opy_ = ET.parse(path)
    bstack1l11111l_opy_ = bstack11l1l111l_opy_.getroot()
    bstack1l111ll1l_opy_ = None
    for suite in bstack1l11111l_opy_.iter(bstack1l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಋ")):
      if bstack1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ಌ") in suite.attrib:
        suite.attrib[bstack1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ಍")] += bstack1l_opy_ (u"ࠨࠢࠪಎ") + bstack1l111ll1_opy_
        bstack1l111ll1l_opy_ = suite
    bstack11ll11_opy_ = None
    for robot in bstack1l11111l_opy_.iter(bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಏ")):
      bstack11ll11_opy_ = robot
    bstack1l1lllll_opy_ = len(bstack11ll11_opy_.findall(bstack1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩಐ")))
    if bstack1l1lllll_opy_ == 1:
      bstack11ll11_opy_.remove(bstack11ll11_opy_.findall(bstack1l_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ಑"))[0])
      bstack11l1l11l1_opy_ = ET.Element(bstack1l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಒ"), attrib={bstack1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಓ"):bstack1l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧಔ"), bstack1l_opy_ (u"ࠨ࡫ࡧࠫಕ"):bstack1l_opy_ (u"ࠩࡶ࠴ࠬಖ")})
      bstack11ll11_opy_.insert(1, bstack11l1l11l1_opy_)
      bstack1l1lllll1_opy_ = None
      for suite in bstack11ll11_opy_.iter(bstack1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩಗ")):
        bstack1l1lllll1_opy_ = suite
      bstack1l1lllll1_opy_.append(bstack1l111ll1l_opy_)
      bstack11ll1_opy_ = None
      for status in bstack1l111ll1l_opy_.iter(bstack1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫಘ")):
        bstack11ll1_opy_ = status
      bstack1l1lllll1_opy_.append(bstack11ll1_opy_)
    bstack11l1l111l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪಙ") + str(e))
def bstack1l1l1l1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l11ll1ll_opy_
  global CONFIG
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥಚ") in options:
    del options[bstack1l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦಛ")]
  if ROBOT_VERSION < bstack1l_opy_ (u"ࠣ࠶࠱࠴ࠧಜ"):
    stats = {
      bstack1l_opy_ (u"ࠤࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠦಝ"): {bstack1l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࠤಞ"): 0, bstack1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦಟ"): 0, bstack1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧಠ"): 0},
      bstack1l_opy_ (u"ࠨࡡ࡭࡮ࠥಡ"): {bstack1l_opy_ (u"ࠢࡵࡱࡷࡥࡱࠨಢ"): 0, bstack1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಣ"): 0, bstack1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤತ"): 0},
    }
  else:
    stats = {
      bstack1l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࠤಥ"): 0,
      bstack1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦದ"): 0,
      bstack1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧಧ"): 0,
      bstack1l_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢನ"): 0,
    }
  bstack1l11l11l1_opy_ = bstack1l1111l1_opy_()
  for bstack1lll1l1l_opy_ in bstack1l11l11l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l_opy_ (u"ࠧࡱࡣࡥࡳࡹࡥࡲࡦࡵࡸࡰࡹࡹࠧ಩"), str(bstack1lll1l1l_opy_), bstack1l_opy_ (u"ࠨࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠬಪ"))
    bstack1llll1l_opy_(path, bstack1l1l11lll_opy_(bstack1l11l11l1_opy_[bstack1lll1l1l_opy_]))
  bstack11111l1l_opy_()
  return bstack1l11ll1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l1l1l_opy_(self, ff_profile_dir):
  global bstack1l11lllll_opy_
  if not ff_profile_dir:
    return None
  return bstack1l11lllll_opy_(self, ff_profile_dir)
def bstack1l111l11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll11l11l_opy_
  bstack1l111l_opy_ = []
  if bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಫ") in CONFIG:
    bstack1l111l_opy_ = CONFIG[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಬ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧಭ")],
      pabot_args[bstack1l_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨಮ")],
      argfile,
      pabot_args.get(bstack1l_opy_ (u"ࠨࡨࡪࡸࡨࠦಯ")),
      pabot_args[bstack1l_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵࠥರ")],
      platform[0],
      bstack1ll11l11l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣಱ")] or [(bstack1l_opy_ (u"ࠤࠥಲ"), None)]
    for platform in enumerate(bstack1l111l_opy_)
  ]
def bstack1l11llll_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11lllllll_opy_=bstack1l_opy_ (u"ࠪࠫಳ")):
  global bstack1111l1_opy_
  self.platform_index = platform_index
  self.bstack11llll111_opy_ = bstack11lllllll_opy_
  bstack1111l1_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1l1111l1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111l_opy_
  global bstack1l1l11ll_opy_
  if not bstack1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭಴") in item.options:
    item.options[bstack1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧವ")] = []
  for v in item.options[bstack1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಶ")]:
    if bstack1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ಷ") in v:
      item.options[bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಸ")].remove(v)
    if bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩಹ") in v:
      item.options[bstack1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ಺")].remove(v)
  item.options[bstack1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭಻")].insert(0, bstack1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃ಼ࠧ").format(item.platform_index))
  item.options[bstack1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಽ")].insert(0, bstack1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࠾ࢀࢃࠧಾ").format(item.bstack11llll111_opy_))
  if bstack1l1l11ll_opy_:
    item.options[bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಿ")].insert(0, bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬೀ").format(bstack1l1l11ll_opy_))
  return bstack111l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack11l11_opy_(command, item_index):
  global bstack1l1l11ll_opy_
  if bstack1l1l11ll_opy_:
    command[0] = command[0].replace(bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩು"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨೂ") + str(item_index) + bstack1l1l11ll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫೃ"), bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪೄ") + str(item_index), 1)
def bstack1l1ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1l111l_opy_
  bstack11l11_opy_(command, item_index)
  return bstack1l1l111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l1llll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1l111l_opy_
  bstack11l11_opy_(command, item_index)
  return bstack1l1l111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1l111l_opy_
  bstack11l11_opy_(command, item_index)
  return bstack1l1l111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1l111lll1_opy_(self, runner, quiet=False, capture=True):
  global bstack1lll11lll_opy_
  bstack1l111111_opy_ = bstack1lll11lll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ೅")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬೆ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l111111_opy_
def bstack1l1l1l11_opy_(self, name, context, *args):
  global bstack1ll11111_opy_
  if name in [bstack1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪೇ"), bstack1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬೈ")]:
    bstack1ll11111_opy_(self, name, context, *args)
  if name == bstack1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ೉"):
    try:
      if(not bstack11llll_opy_):
        bstack1ll11l1_opy_ = str(self.feature.name)
        bstack11lll11ll_opy_(context, bstack1ll11l1_opy_)
        context.browser.execute_script(bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪೊ") + json.dumps(bstack1ll11l1_opy_) + bstack1l_opy_ (u"࠭ࡽࡾࠩೋ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧೌ").format(str(e)))
  if name == bstack1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ್ࠪ"):
    try:
      if not hasattr(self, bstack1l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೎")):
        self.driver_before_scenario = True
      if(not bstack11llll_opy_):
        bstack1llll11l_opy_ = args[0].name
        bstack1111l1ll_opy_ = bstack1ll11l1_opy_ = str(self.feature.name)
        bstack1ll11l1_opy_ = bstack1111l1ll_opy_ + bstack1l_opy_ (u"ࠪࠤ࠲ࠦࠧ೏") + bstack1llll11l_opy_
        if self.driver_before_scenario:
          bstack11lll11ll_opy_(context, bstack1ll11l1_opy_)
          context.browser.execute_script(bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ೐") + json.dumps(bstack1ll11l1_opy_) + bstack1l_opy_ (u"ࠬࢃࡽࠨ೑"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ೒").format(str(e)))
  if name == bstack1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ೓"):
    try:
      bstack1lllllll_opy_ = args[0].status.name
      if str(bstack1lllllll_opy_).lower() == bstack1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ೔"):
        bstack111llll1_opy_ = bstack1l_opy_ (u"ࠩࠪೕ")
        bstack111ll1l_opy_ = bstack1l_opy_ (u"ࠪࠫೖ")
        bstack111ll11_opy_ = bstack1l_opy_ (u"ࠫࠬ೗")
        try:
          import traceback
          bstack111llll1_opy_ = self.exception.__class__.__name__
          bstack11ll11l1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack111ll1l_opy_ = bstack1l_opy_ (u"ࠬࠦࠧ೘").join(bstack11ll11l1l_opy_)
          bstack111ll11_opy_ = bstack11ll11l1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack11l111l1_opy_.format(str(e)))
        bstack111llll1_opy_ += bstack111ll11_opy_
        bstack1111_opy_(context, json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ೙") + str(bstack111ll1l_opy_)), bstack1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ೚"))
        if self.driver_before_scenario:
          bstack11l1_opy_(context, bstack1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ೛"), bstack111llll1_opy_)
        context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ೜") + json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤೝ") + str(bstack111ll1l_opy_)) + bstack1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫೞ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬ೟") + json.dumps(bstack1l_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥೠ") + str(bstack111llll1_opy_)) + bstack1l_opy_ (u"ࠧࡾࡿࠪೡ"))
      else:
        bstack1111_opy_(context, bstack1l_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤೢ"), bstack1l_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢೣ"))
        if self.driver_before_scenario:
          bstack11l1_opy_(context, bstack1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ೤"))
        context.browser.execute_script(bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ೥") + json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ೦")) + bstack1l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ೧"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡲࡤࡷࡸ࡫ࡤࠣࡿࢀࠫ೨"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ೩").format(str(e)))
  if name == bstack1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ೪"):
    try:
      if context.failed is True:
        bstack1ll111l11_opy_ = []
        bstack1lll111ll_opy_ = []
        bstack1l11ll11_opy_ = []
        bstack11l1llll_opy_ = bstack1l_opy_ (u"ࠪࠫ೫")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll111l11_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack11ll11l1l_opy_ = traceback.format_tb(exc_tb)
            bstack1l111_opy_ = bstack1l_opy_ (u"ࠫࠥ࠭೬").join(bstack11ll11l1l_opy_)
            bstack1lll111ll_opy_.append(bstack1l111_opy_)
            bstack1l11ll11_opy_.append(bstack11ll11l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack11l111l1_opy_.format(str(e)))
        bstack111llll1_opy_ = bstack1l_opy_ (u"ࠬ࠭೭")
        for i in range(len(bstack1ll111l11_opy_)):
          bstack111llll1_opy_ += bstack1ll111l11_opy_[i] + bstack1l11ll11_opy_[i] + bstack1l_opy_ (u"࠭࡜࡯ࠩ೮")
        bstack11l1llll_opy_ = bstack1l_opy_ (u"ࠧࠡࠩ೯").join(bstack1lll111ll_opy_)
        if not self.driver_before_scenario:
          bstack1111_opy_(context, bstack11l1llll_opy_, bstack1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ೰"))
          bstack11l1_opy_(context, bstack1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤೱ"), bstack111llll1_opy_)
          context.browser.execute_script(bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨೲ") + json.dumps(bstack11l1llll_opy_) + bstack1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫೳ"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬ೴") + json.dumps(bstack1l_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦ೵") + str(bstack111llll1_opy_)) + bstack1l_opy_ (u"ࠧࡾࡿࠪ೶"))
      else:
        if not self.driver_before_scenario:
          bstack1111_opy_(context, bstack1l_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦ೷") + str(self.feature.name) + bstack1l_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦ೸"), bstack1l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣ೹"))
          bstack11l1_opy_(context, bstack1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ೺"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ೻") + json.dumps(bstack1l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ೼") + str(self.feature.name) + bstack1l_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ೽")) + bstack1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ೾"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡴࡦࡹࡳࡦࡦࠥࢁࢂ࠭೿"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬഀ").format(str(e)))
  if name in [bstack1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫഁ"), bstack1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ം")]:
    bstack1ll11111_opy_(self, name, context, *args)
    if (name == bstack1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഃ") and self.driver_before_scenario) or (name == bstack1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧഄ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack111l1l1l_opy_(config, startdir):
  return bstack1l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨഅ").format(bstack1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣആ"))
class Notset:
  def __repr__(self):
    return bstack1l_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧഇ")
notset = Notset()
def bstack1l1l111_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll111111_opy_
  if str(name).lower() == bstack1l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫഈ"):
    return bstack1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦഉ")
  else:
    return bstack1ll111111_opy_(self, name, default, skip)
def bstack1ll1lll_opy_(item, when):
  global bstack1ll1l11ll_opy_
  try:
    bstack1ll1l11ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1l1l11l_opy_():
  return
def bstack1ll1111l1_opy_(bstack1ll1lll1_opy_):
  global bstack11l1ll111_opy_
  global bstack1l1l1l1l_opy_
  bstack11l1ll111_opy_ = bstack1ll1lll1_opy_
  logger.info(bstack1ll1ll1_opy_.format(bstack11l1ll111_opy_.split(bstack1l_opy_ (u"࠭࠭ࠨഊ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack111111l_opy_
    Service.stop = bstack111ll111_opy_
    webdriver.Remote.__init__ = bstack1llllllll_opy_
    webdriver.Remote.get = bstack1l1lll1ll_opy_
    WebDriver.close = bstack111l11l_opy_
    bstack1l1l1l1l_opy_ = True
  except Exception as e:
    pass
  bstack1l1lll11_opy_()
  if not bstack1l1l1l1l_opy_:
    bstack1l111l1_opy_(bstack1l_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤഋ"), bstack1l1l1l1l1_opy_)
  if bstack1l1lll1l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11l1l1l1_opy_
    except Exception as e:
      logger.error(bstack1lll11_opy_.format(str(e)))
  if (bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧഌ") in str(bstack1ll1lll1_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l1l1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l1ll1lll_opy_
      except Exception as e:
        logger.warn(bstack111lll_opy_ + str(e))
    except Exception as e:
      bstack1l111l1_opy_(e, bstack111lll_opy_)
    Output.end_test = bstack1l1l1ll1_opy_
    TestStatus.__init__ = bstack111ll11l_opy_
    QueueItem.__init__ = bstack1l11llll_opy_
    pabot._create_items = bstack1l111l11_opy_
    try:
      from pabot import __version__ as bstack111111l1_opy_
      if version.parse(bstack111111l1_opy_) >= version.parse(bstack1l_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩ഍")):
        pabot._run = bstack1l111ll_opy_
      elif version.parse(bstack111111l1_opy_) >= version.parse(bstack1l_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪഎ")):
        pabot._run = bstack11l1llll1_opy_
      else:
        pabot._run = bstack1l1ll111l_opy_
    except Exception as e:
      pabot._run = bstack1l1ll111l_opy_
    pabot._create_command_for_execution = bstack1l1111l1l_opy_
    pabot._report_results = bstack1l1l1l1ll_opy_
  if bstack1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഏ") in str(bstack1ll1lll1_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l111l1_opy_(e, bstack1llll1l1_opy_)
    Runner.run_hook = bstack1l1l1l11_opy_
    Step.run = bstack1l111lll1_opy_
  if bstack1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬഐ") in str(bstack1ll1lll1_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack111l1l1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1l1l11l_opy_
      Config.getoption = bstack1l1l111_opy_
      runner._update_current_test_var = bstack1ll1lll_opy_
    except Exception as e:
      pass
def bstack1l11l111_opy_():
  global CONFIG
  if bstack1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭഑") in CONFIG and int(CONFIG[bstack1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧഒ")]) > 1:
    logger.warn(bstack1llllll1_opy_)
def bstack1llll1l1l_opy_(bstack1l111lll_opy_, index):
  bstack1ll1111l1_opy_(bstack1lll1_opy_)
  exec(open(bstack1l111lll_opy_).read())
def bstack11lll1111_opy_(arg):
  arg.append(bstack1l_opy_ (u"ࠣ࠯࠰ࡧࡦࡶࡴࡶࡴࡨࡁࡸࡿࡳࠣഓ"))
  arg.append(bstack1l_opy_ (u"ࠤ࠰࡛ࠧഔ"))
  arg.append(bstack1l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨക"))
  global CONFIG
  bstack1ll1111l1_opy_(bstack11ll1111l_opy_)
  os.environ[bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬഖ")] = CONFIG[bstack1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഗ")]
  os.environ[bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩഘ")] = CONFIG[bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪങ")]
  from _pytest.config import main as bstack1l11ll1_opy_
  bstack1l11ll1_opy_(arg)
def bstack1llll11ll_opy_(arg):
  bstack1ll1111l1_opy_(bstack1ll1111ll_opy_)
  from behave.__main__ import main as bstack11111ll_opy_
  bstack11111ll_opy_(arg)
def bstack11l1l1ll_opy_():
  logger.info(bstack1ll11l11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧച"), help=bstack1l_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪഛ"))
  parser.add_argument(bstack1l_opy_ (u"ࠪ࠱ࡺ࠭ജ"), bstack1l_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨഝ"), help=bstack1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫഞ"))
  parser.add_argument(bstack1l_opy_ (u"࠭࠭࡬ࠩട"), bstack1l_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ഠ"), help=bstack1l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩഡ"))
  parser.add_argument(bstack1l_opy_ (u"ࠩ࠰ࡪࠬഢ"), bstack1l_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨണ"), help=bstack1l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪത"))
  bstack11lllll11_opy_ = parser.parse_args()
  try:
    bstack1l1l1l_opy_ = bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩഥ")
    if bstack11lllll11_opy_.framework and bstack11lllll11_opy_.framework not in (bstack1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ദ"), bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨധ")):
      bstack1l1l1l_opy_ = bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧന")
    bstack1lll1lll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1l_opy_)
    bstack1ll1ll1l_opy_ = open(bstack1lll1lll_opy_, bstack1l_opy_ (u"ࠩࡵࠫഩ"))
    bstack11ll1l1l1_opy_ = bstack1ll1ll1l_opy_.read()
    bstack1ll1ll1l_opy_.close()
    if bstack11lllll11_opy_.username:
      bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_.replace(bstack1l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪപ"), bstack11lllll11_opy_.username)
    if bstack11lllll11_opy_.key:
      bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_.replace(bstack1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ഫ"), bstack11lllll11_opy_.key)
    if bstack11lllll11_opy_.framework:
      bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_.replace(bstack1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ബ"), bstack11lllll11_opy_.framework)
    file_name = bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩഭ")
    file_path = os.path.abspath(file_name)
    bstack1ll111l1l_opy_ = open(file_path, bstack1l_opy_ (u"ࠧࡸࠩമ"))
    bstack1ll111l1l_opy_.write(bstack11ll1l1l1_opy_)
    bstack1ll111l1l_opy_.close()
    logger.info(bstack111lll1_opy_)
    try:
      os.environ[bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪയ")] = bstack11lllll11_opy_.framework if bstack11lllll11_opy_.framework != None else bstack1l_opy_ (u"ࠤࠥര")
      config = yaml.safe_load(bstack11ll1l1l1_opy_)
      config[bstack1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪറ")] = bstack1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪല")
      bstack11ll111l1_opy_(bstack11lll1l11_opy_, config)
    except Exception as e:
      logger.debug(bstack11ll11ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1l1ll1_opy_.format(str(e)))
def bstack11ll111l1_opy_(bstack1ll1ll111_opy_, config, bstack1l1ll11_opy_ = {}):
  global bstack1l111l11l_opy_
  if not config:
    return
  bstack1l11lll1l_opy_ = bstack111111_opy_ if not bstack1l111l11l_opy_ else ( bstack1ll1l11_opy_ if bstack1l_opy_ (u"ࠬࡧࡰࡱࠩള") in config else bstack11ll1l1_opy_ )
  data = {
    bstack1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨഴ"): config[bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩവ")],
    bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫശ"): config[bstack1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬഷ")],
    bstack1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧസ"): bstack1ll1ll111_opy_,
    bstack1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧഹ"): {
      bstack1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪഺ"): str(config[bstack1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ഻࠭")]) if bstack1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫഼ࠧ") in config else bstack1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤഽ"),
      bstack1l_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫാ"): bstack11lll1l_opy_(os.getenv(bstack1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧി"), bstack1l_opy_ (u"ࠦࠧീ"))),
      bstack1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧു"): bstack1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ൂ"),
      bstack1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨൃ"): bstack1l11lll1l_opy_,
      bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫൄ"): config[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ൅")]if config[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭െ")] else bstack1l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧേ"),
      bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧൈ"): str(config[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ൉")]) if bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩൊ") in config else bstack1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤോ"),
      bstack1l_opy_ (u"ࠩࡲࡷࠬൌ"): sys.platform,
      bstack1l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩ്ࠬ"): socket.gethostname()
    }
  }
  update(data[bstack1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൎ")], bstack1l1ll11_opy_)
  try:
    response = bstack11l1l1_opy_(bstack1l_opy_ (u"ࠬࡖࡏࡔࡖࠪ൏"), bstack1ll11lll1_opy_, data, config)
    if response:
      logger.debug(bstack1l111ll11_opy_.format(bstack1ll1ll111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lllll1ll_opy_.format(str(e)))
def bstack11l1l1_opy_(type, url, data, config):
  bstack1ll11l1ll_opy_ = bstack1ll1ll1ll_opy_.format(url)
  proxy = bstack1ll11111l_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ൐")) or config.get(bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ൑")):
    proxies = {
      bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ൒"): proxy
    }
  if type == bstack1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ൓"):
    response = requests.post(bstack1ll11l1ll_opy_, json=data,
                    headers={bstack1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩൔ"): bstack1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧൕ")}, auth=(config[bstack1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧൖ")], config[bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩൗ")]), proxies=proxies)
  return response
def bstack11lll1l_opy_(framework):
  return bstack1l_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦ൘").format(str(framework), __version__) if framework else bstack1l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ൙").format(__version__)
def bstack11l111l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1lllll1l_opy_()
    logger.debug(bstack1111llll_opy_.format(str(CONFIG)))
    bstack1ll11ll1l_opy_()
    bstack11l1l1111_opy_()
  except Exception as e:
    logger.error(bstack1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨ൚") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll1l1111_opy_
  atexit.register(bstack1ll1l111_opy_)
  signal.signal(signal.SIGINT, bstack1l111llll_opy_)
  signal.signal(signal.SIGTERM, bstack1l111llll_opy_)
def bstack1ll1l1111_opy_(exctype, value, traceback):
  global bstack11ll_opy_
  try:
    for driver in bstack11ll_opy_:
      driver.execute_script(
        bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠢࠪ൛") + json.dumps(bstack1l_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ൜") + str(value)) + bstack1l_opy_ (u"ࠬࢃࡽࠨ൝"))
  except Exception:
    pass
  bstack1l11l11l_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l11l11l_opy_(message = bstack1l_opy_ (u"࠭ࠧ൞")):
  global CONFIG
  try:
    if message:
      bstack1l1ll11_opy_ = {
        bstack1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ൟ"): str(message)
      }
      bstack11ll111l1_opy_(bstack11l1l1ll1_opy_, CONFIG, bstack1l1ll11_opy_)
    else:
      bstack11ll111l1_opy_(bstack11l1l1ll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lllll1l1_opy_.format(str(e)))
def bstack1l1ll111_opy_(bstack111l1_opy_, size):
  bstack1ll1l1lll_opy_ = []
  while len(bstack111l1_opy_) > size:
    bstack11l1l1l1l_opy_ = bstack111l1_opy_[:size]
    bstack1ll1l1lll_opy_.append(bstack11l1l1l1l_opy_)
    bstack111l1_opy_   = bstack111l1_opy_[size:]
  bstack1ll1l1lll_opy_.append(bstack111l1_opy_)
  return bstack1ll1l1lll_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack11111l11_opy_)
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫൠ")  or sys.argv[1] == bstack1l_opy_ (u"ࠩ࠰ࡺࠬൡ"):
    logger.info(bstack1l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪൢ").format(__version__))
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪൣ"):
    bstack11l1l1ll_opy_()
    return
  args = sys.argv
  bstack11l111l_opy_()
  global CONFIG
  global bstack11l1ll11l_opy_
  global bstack11ll1l11l_opy_
  global bstack1l1111ll1_opy_
  global bstack1ll11l11l_opy_
  global bstack1l1l11ll_opy_
  bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠬ࠭൤")
  if args[1] == bstack1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൥") or args[1] == bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ൦"):
    bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ൧")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൨"):
    bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൩")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൪"):
    bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൫")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ൬"):
    bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ൭")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ൮"):
    bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ൯")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ൰"):
    bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൱")
    args = args[2:]
  else:
    if not bstack1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ൲") in CONFIG or str(CONFIG[bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ൳")]).lower() in [bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൴"), bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ൵")]:
      bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ൶")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൷")]).lower() == bstack1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ൸"):
      bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ൹")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩൺ")]).lower() == bstack1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ൻ"):
      bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧർ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൽ")]).lower() == bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪൾ"):
      bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫൿ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ඀")]).lower() == bstack1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඁ"):
      bstack1l111l111_opy_ = bstack1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧං")
      args = args[1:]
    else:
      os.environ[bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪඃ")] = bstack1l111l111_opy_
      bstack1l11l1lll_opy_(bstack1l1ll1ll_opy_)
  global bstack1l1111l_opy_
  try:
    os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ඄")] = bstack1l111l111_opy_
    bstack11ll111l1_opy_(bstack111l1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lllll1l1_opy_.format(str(e)))
  global bstack1ll111lll_opy_
  global bstack111lll1l_opy_
  global bstack1llll1111_opy_
  global bstack11l1lll_opy_
  global bstack1l11lllll_opy_
  global bstack1l1l111l_opy_
  global bstack1111l1_opy_
  global bstack111l_opy_
  global bstack1ll111l_opy_
  global bstack1ll11111_opy_
  global bstack1lll11lll_opy_
  global bstack1ll1lllll_opy_
  global bstack1ll1l1ll_opy_
  global bstack1ll111111_opy_
  global bstack1ll1l11ll_opy_
  global bstack1l11ll1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll111lll_opy_ = webdriver.Remote.__init__
    bstack1ll111l_opy_ = WebDriver.close
    bstack1ll1lllll_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1111l_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack111l11ll_opy_():
    if bstack1ll11ll1_opy_() < version.parse(bstack11ll1111_opy_):
      logger.error(bstack1l1l11l1l_opy_.format(bstack1ll11ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll1l1ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1lll11_opy_.format(str(e)))
  bstack111l1ll1_opy_()
  if (bstack1l111l111_opy_ in [bstack1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩඅ"), bstack1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪආ"), bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ඇ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l1l1l_opy_
        bstack1llll1111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack111lll_opy_ + str(e))
    except Exception as e:
      bstack1l111l1_opy_(e, bstack111lll_opy_)
    if bstack1l111l111_opy_ != bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧඈ"):
      bstack11111l1l_opy_()
    bstack111lll1l_opy_ = Output.end_test
    bstack11l1lll_opy_ = TestStatus.__init__
    bstack1l1l111l_opy_ = pabot._run
    bstack1111l1_opy_ = QueueItem.__init__
    bstack111l_opy_ = pabot._create_command_for_execution
    bstack1l11ll1ll_opy_ = pabot._report_results
  if bstack1l111l111_opy_ == bstack1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧඉ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l111l1_opy_(e, bstack1llll1l1_opy_)
    bstack1ll11111_opy_ = Runner.run_hook
    bstack1lll11lll_opy_ = Step.run
  if bstack1l111l111_opy_ == bstack1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨඊ"):
    try:
      from _pytest.config import Config
      bstack1ll111111_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll1l11ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1ll1l1l11_opy_)
  if bstack1l111l111_opy_ == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩඋ"):
    bstack1l1lll1l_opy_()
    bstack1l11l111_opy_()
    if bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ඌ") in CONFIG:
      bstack11ll1l11l_opy_ = True
      bstack111l11_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧඍ")]):
        bstack111l11_opy_.append(bstack1l11l1ll_opy_(name=str(index),
                                      target=bstack1llll1l1l_opy_, args=(args[0], index)))
      for t in bstack111l11_opy_:
        t.start()
      for t in bstack111l11_opy_:
        t.join()
    else:
      bstack1ll1111l1_opy_(bstack1lll1_opy_)
      exec(open(args[0]).read())
  elif bstack1l111l111_opy_ == bstack1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫඎ") or bstack1l111l111_opy_ == bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඏ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l111l1_opy_(e, bstack111lll_opy_)
    bstack1l1lll1l_opy_()
    bstack1ll1111l1_opy_(bstack11lll1l1l_opy_)
    if bstack1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬඐ") in args:
      i = args.index(bstack1l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭එ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack11l1ll11l_opy_))
    args.insert(0, str(bstack1l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧඒ")))
    pabot.main(args)
  elif bstack1l111l111_opy_ == bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫඓ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l111l1_opy_(e, bstack111lll_opy_)
    for a in args:
      if bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪඔ") in a:
        bstack1l1111ll1_opy_ = int(a.split(bstack1l_opy_ (u"ࠬࡀࠧඕ"))[1])
      if bstack1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪඖ") in a:
        bstack1ll11l11l_opy_ = str(a.split(bstack1l_opy_ (u"ࠧ࠻ࠩ඗"))[1])
      if bstack1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ඘") in a:
        bstack1l1l11ll_opy_ = str(a.split(bstack1l_opy_ (u"ࠩ࠽ࠫ඙"))[1])
    bstack11ll11ll1_opy_ = None
    if bstack1l_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩක") in args:
      i = args.index(bstack1l_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪඛ"))
      args.pop(i)
      bstack11ll11ll1_opy_ = args.pop(i)
    if bstack11ll11ll1_opy_ is not None:
      global bstack1llllll11_opy_
      bstack1llllll11_opy_ = bstack11ll11ll1_opy_
    bstack1ll1111l1_opy_(bstack11lll1l1l_opy_)
    run_cli(args)
  elif bstack1l111l111_opy_ == bstack1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬග"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack111l1lll_opy_ = importlib.find_loader(bstack1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨඝ"))
    except Exception as e:
      logger.warn(e, bstack1ll1l1l11_opy_)
    bstack1l1lll1l_opy_()
    try:
      if bstack1l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩඞ") in args:
        i = args.index(bstack1l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪඟ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬච") in args:
        i = args.index(bstack1l_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ඡ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠫ࠲ࡶࠧජ") in args:
        i = args.index(bstack1l_opy_ (u"ࠬ࠳ࡰࠨඣ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧඤ") in args:
        i = args.index(bstack1l_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨඥ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠨ࠯ࡱࠫඦ") in args:
        i = args.index(bstack1l_opy_ (u"ࠩ࠰ࡲࠬට"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack11lll1l1_opy_ = config.args
    bstack1ll1ll_opy_ = config.invocation_params.args
    bstack1ll1ll_opy_ = list(bstack1ll1ll_opy_)
    bstack1l11ll111_opy_ = []
    for arg in bstack1ll1ll_opy_:
      for spec in bstack11lll1l1_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1l11ll111_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫඨ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11lll1l1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lll11ll1_opy_)))
                    for bstack1lll11ll1_opy_ in bstack11lll1l1_opy_]
    if (bstack11llll_opy_):
      bstack1l11ll111_opy_.append(bstack1l_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨඩ"))
      bstack1l11ll111_opy_.append(bstack1l_opy_ (u"࡚ࠬࡲࡶࡧࠪඪ"))
    bstack1l11ll111_opy_.append(bstack1l_opy_ (u"࠭࠭ࡱࠩණ"))
    bstack1l11ll111_opy_.append(bstack1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬඬ"))
    bstack1l11ll111_opy_.append(bstack1l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪත"))
    bstack1l11ll111_opy_.append(bstack1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩථ"))
    bstack1l1llll_opy_ = []
    for spec in bstack11lll1l1_opy_:
      bstack111ll1l1_opy_ = []
      bstack111ll1l1_opy_.append(spec)
      bstack111ll1l1_opy_ += bstack1l11ll111_opy_
      bstack1l1llll_opy_.append(bstack111ll1l1_opy_)
    bstack11ll1l11l_opy_ = True
    bstack1l11111_opy_ = 1
    if bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪද") in CONFIG:
      bstack1l11111_opy_ = CONFIG[bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫධ")]
    bstack1l1l1ll_opy_ = int(bstack1l11111_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨන")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ඲")]):
      for bstack111ll1l1_opy_ in bstack1l1llll_opy_:
        item = {}
        item[bstack1l_opy_ (u"ࠧࡢࡴࡪࠫඳ")] = bstack111ll1l1_opy_
        item[bstack1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧප")] = index
        execution_items.append(item)
    bstack1111l1l1_opy_ = bstack1l1ll111_opy_(execution_items, bstack1l1l1ll_opy_)
    for execution_item in bstack1111l1l1_opy_:
      bstack111l11_opy_ = []
      for item in execution_item:
        bstack111l11_opy_.append(bstack1l11l1ll_opy_(name=str(item[bstack1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨඵ")]),
                                            target=bstack11lll1111_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠪࡥࡷ࡭ࠧබ")],)))
      for t in bstack111l11_opy_:
        t.start()
      for t in bstack111l11_opy_:
        t.join()
  elif bstack1l111l111_opy_ == bstack1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫභ"):
    try:
      from behave.__main__ import main as bstack11111ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l111l1_opy_(e, bstack1llll1l1_opy_)
    bstack1l1lll1l_opy_()
    bstack11ll1l11l_opy_ = True
    bstack1l11111_opy_ = 1
    if bstack1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬම") in CONFIG:
      bstack1l11111_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ඹ")]
    bstack1l1l1ll_opy_ = int(bstack1l11111_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪය")]))
    config = Configuration(args)
    bstack11lll1l1_opy_ = config.paths
    bstack1l11l11ll_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack11lll1l1_opy_:
        bstack1l11l11ll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩර"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11lll1l1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lll11ll1_opy_)))
                    for bstack1lll11ll1_opy_ in bstack11lll1l1_opy_]
    bstack1l1llll_opy_ = []
    for spec in bstack11lll1l1_opy_:
      bstack111ll1l1_opy_ = []
      bstack111ll1l1_opy_ += bstack1l11l11ll_opy_
      bstack111ll1l1_opy_.append(spec)
      bstack1l1llll_opy_.append(bstack111ll1l1_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ඼")]):
      for bstack111ll1l1_opy_ in bstack1l1llll_opy_:
        item = {}
        item[bstack1l_opy_ (u"ࠪࡥࡷ࡭ࠧල")] = bstack1l_opy_ (u"ࠫࠥ࠭඾").join(bstack111ll1l1_opy_)
        item[bstack1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ඿")] = index
        execution_items.append(item)
    bstack1111l1l1_opy_ = bstack1l1ll111_opy_(execution_items, bstack1l1l1ll_opy_)
    for execution_item in bstack1111l1l1_opy_:
      bstack111l11_opy_ = []
      for item in execution_item:
        bstack111l11_opy_.append(bstack1l11l1ll_opy_(name=str(item[bstack1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬව")]),
                                            target=bstack1llll11ll_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠧࡢࡴࡪࠫශ")],)))
      for t in bstack111l11_opy_:
        t.start()
      for t in bstack111l11_opy_:
        t.join()
  else:
    bstack1l11l1lll_opy_(bstack1l1ll1ll_opy_)
  bstack1111lll_opy_()
def bstack1111lll_opy_():
  [bstack1l11111ll_opy_, bstack111ll_opy_] = bstack1l1lll_opy_()
  if bstack1l11111ll_opy_ is not None and bstack1111lll1_opy_() != -1:
    sessions = bstack1ll11lll_opy_(bstack1l11111ll_opy_)
    bstack11ll11l11_opy_(sessions, bstack111ll_opy_)
def bstack1ll1ll11l_opy_(bstack1l1lll111_opy_):
    if bstack1l1lll111_opy_:
        return bstack1l1lll111_opy_.capitalize()
    else:
        return bstack1l1lll111_opy_
def bstack11111111_opy_(bstack11ll1ll1l_opy_):
    if bstack1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ෂ") in bstack11ll1ll1l_opy_ and bstack11ll1ll1l_opy_[bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧස")] != bstack1l_opy_ (u"ࠪࠫහ"):
        return bstack11ll1ll1l_opy_[bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩළ")]
    else:
        bstack1lll1l11_opy_ = bstack1l_opy_ (u"ࠧࠨෆ")
        if bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭෇") in bstack11ll1ll1l_opy_ and bstack11ll1ll1l_opy_[bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ෈")] != None:
            bstack1lll1l11_opy_ += bstack11ll1ll1l_opy_[bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ෉")] + bstack1l_opy_ (u"ࠤ࠯ࠤ්ࠧ")
            if bstack11ll1ll1l_opy_[bstack1l_opy_ (u"ࠪࡳࡸ࠭෋")] == bstack1l_opy_ (u"ࠦ࡮ࡵࡳࠣ෌"):
                bstack1lll1l11_opy_ += bstack1l_opy_ (u"ࠧ࡯ࡏࡔࠢࠥ෍")
            bstack1lll1l11_opy_ += (bstack11ll1ll1l_opy_[bstack1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ෎")] or bstack1l_opy_ (u"ࠧࠨා"))
            return bstack1lll1l11_opy_
        else:
            bstack1lll1l11_opy_ += bstack1ll1ll11l_opy_(bstack11ll1ll1l_opy_[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩැ")]) + bstack1l_opy_ (u"ࠤࠣࠦෑ") + (bstack11ll1ll1l_opy_[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬි")] or bstack1l_opy_ (u"ࠫࠬී")) + bstack1l_opy_ (u"ࠧ࠲ࠠࠣු")
            if bstack11ll1ll1l_opy_[bstack1l_opy_ (u"࠭࡯ࡴࠩ෕")] == bstack1l_opy_ (u"ࠢࡘ࡫ࡱࡨࡴࡽࡳࠣූ"):
                bstack1lll1l11_opy_ += bstack1l_opy_ (u"࡙ࠣ࡬ࡲࠥࠨ෗")
            bstack1lll1l11_opy_ += bstack11ll1ll1l_opy_[bstack1l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ෘ")] or bstack1l_opy_ (u"ࠪࠫෙ")
            return bstack1lll1l11_opy_
def bstack1l1ll1l1_opy_(bstack1ll1l_opy_):
    if bstack1ll1l_opy_ == bstack1l_opy_ (u"ࠦࡩࡵ࡮ࡦࠤේ"):
        return bstack1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡄࡱࡰࡴࡱ࡫ࡴࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨෛ")
    elif bstack1ll1l_opy_ == bstack1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨො"):
        return bstack1l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡌࡡࡪ࡮ࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪෝ")
    elif bstack1ll1l_opy_ == bstack1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣෞ"):
        return bstack1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡕࡧࡳࡴࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩෟ")
    elif bstack1ll1l_opy_ == bstack1l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ෠"):
        return bstack1l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡈࡶࡷࡵࡲ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭෡")
    elif bstack1ll1l_opy_ == bstack1l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨ෢"):
        return bstack1l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࠥࡨࡩࡦ࠹࠲࠷࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࠧࡪ࡫ࡡ࠴࠴࠹ࠦࡃ࡚ࡩ࡮ࡧࡲࡹࡹࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ෣")
    elif bstack1ll1l_opy_ == bstack1l_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠣ෤"):
        return bstack1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࡖࡺࡴ࡮ࡪࡰࡪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ෥")
    else:
        return bstack1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃ࠭෦")+bstack1ll1ll11l_opy_(bstack1ll1l_opy_)+bstack1l_opy_ (u"ࠪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ෧")
def bstack11llll11_opy_(session):
    return bstack1l_opy_ (u"ࠫࡁࡺࡲࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡴࡲࡻࠧࡄ࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠡࡵࡨࡷࡸ࡯࡯࡯࠯ࡱࡥࡲ࡫ࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࡿࢂࠨࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣࡡࡥࡰࡦࡴ࡫ࠣࡀࡾࢁࡁ࠵ࡡ࠿࠾࠲ࡸࡩࡄࡻࡾࡽࢀࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂ࠯ࡵࡴࡁࠫ෨").format(session[bstack1l_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩ෩")],bstack11111111_opy_(session), bstack1l1ll1l1_opy_(session[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠬ෪")]), bstack1l1ll1l1_opy_(session[bstack1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ෫")]), bstack1ll1ll11l_opy_(session[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ෬")] or session[bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ෭")] or bstack1l_opy_ (u"ࠪࠫ෮")) + bstack1l_opy_ (u"ࠦࠥࠨ෯") + (session[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ෰")] or bstack1l_opy_ (u"࠭ࠧ෱")), session[bstack1l_opy_ (u"ࠧࡰࡵࠪෲ")] + bstack1l_opy_ (u"ࠣࠢࠥෳ") + session[bstack1l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭෴")], session[bstack1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ෵")] or bstack1l_opy_ (u"ࠫࠬ෶"), session[bstack1l_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ෷")] if session[bstack1l_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪ෸")] else bstack1l_opy_ (u"ࠧࠨ෹"))
def bstack11ll11l11_opy_(sessions, bstack111ll_opy_):
  try:
    bstack1lllll11l_opy_ = bstack1l_opy_ (u"ࠣࠤ෺")
    if not os.path.exists(bstack111l111_opy_):
      os.mkdir(bstack111l111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l_opy_ (u"ࠩࡤࡷࡸ࡫ࡴࡴ࠱ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧ෻")), bstack1l_opy_ (u"ࠪࡶࠬ෼")) as f:
      bstack1lllll11l_opy_ = f.read()
    bstack1lllll11l_opy_ = bstack1lllll11l_opy_.replace(bstack1l_opy_ (u"ࠫࢀࠫࡒࡆࡕࡘࡐ࡙࡙࡟ࡄࡑࡘࡒ࡙ࠫࡽࠨ෽"), str(len(sessions)))
    bstack1lllll11l_opy_ = bstack1lllll11l_opy_.replace(bstack1l_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡕࡓࡎࠨࢁࠬ෾"), bstack111ll_opy_)
    bstack1lllll11l_opy_ = bstack1lllll11l_opy_.replace(bstack1l_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠪࢃࠧ෿"), sessions[0].get(bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡢ࡯ࡨࠫ฀")) if sessions[0] else bstack1l_opy_ (u"ࠨࠩก"))
    with open(os.path.join(bstack111l111_opy_, bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ข")), bstack1l_opy_ (u"ࠪࡻࠬฃ")) as stream:
      stream.write(bstack1lllll11l_opy_.split(bstack1l_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨค"))[0])
      for session in sessions:
        stream.write(bstack11llll11_opy_(session))
      stream.write(bstack1lllll11l_opy_.split(bstack1l_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩฅ"))[1])
    logger.info(bstack1l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡤࡸ࡭ࡱࡪࠠࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠣࡥࡹࠦࡻࡾࠩฆ").format(bstack111l111_opy_));
  except Exception as e:
    logger.debug(bstack11l1ll1l_opy_.format(str(e)))
def bstack1ll11lll_opy_(bstack1l11111ll_opy_):
  global CONFIG
  try:
    host = bstack1l_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪง") if bstack1l_opy_ (u"ࠨࡣࡳࡴࠬจ") in CONFIG else bstack1l_opy_ (u"ࠩࡤࡴ࡮࠭ฉ")
    user = CONFIG[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬช")]
    key = CONFIG[bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧซ")]
    bstack11111l_opy_ = bstack1l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫฌ") if bstack1l_opy_ (u"࠭ࡡࡱࡲࠪญ") in CONFIG else bstack1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩฎ")
    url = bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭ฏ").format(user, key, host, bstack11111l_opy_, bstack1l11111ll_opy_)
    headers = {
      bstack1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨฐ"): bstack1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ฑ"),
    }
    proxy = bstack1ll11111l_opy_(CONFIG)
    proxies = {}
    if CONFIG.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧฒ")) or CONFIG.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩณ")):
      proxies = {
        bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬด"): proxy
      }
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬต")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1l1l111_opy_.format(str(e)))
def bstack1l1lll_opy_():
  global CONFIG
  try:
    if bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫถ") in CONFIG:
      host = bstack1l_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬท") if bstack1l_opy_ (u"ࠪࡥࡵࡶࠧธ") in CONFIG else bstack1l_opy_ (u"ࠫࡦࡶࡩࠨน")
      user = CONFIG[bstack1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧบ")]
      key = CONFIG[bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩป")]
      bstack11111l_opy_ = bstack1l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ผ") if bstack1l_opy_ (u"ࠨࡣࡳࡴࠬฝ") in CONFIG else bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫพ")
      url = bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪฟ").format(user, key, host, bstack11111l_opy_)
      headers = {
        bstack1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪภ"): bstack1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨม"),
      }
      if bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨย") in CONFIG:
        params = {bstack1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬร"):CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫฤ")], bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬล"):CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬฦ")]}
      else:
        params = {bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩว"):CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨศ")]}
      proxy = bstack1ll11111l_opy_(CONFIG)
      proxies = {}
      if CONFIG.get(bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩษ")) or CONFIG.get(bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫส")):
        proxies = {
          bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧห"): proxy
        }
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11l1l11_opy_ = response.json()[0][bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬฬ")]
        if bstack11l1l11_opy_:
          bstack111ll_opy_ = bstack11l1l11_opy_[bstack1l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧอ")].split(bstack1l_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪฮ"))[0] + bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭ฯ") + bstack11l1l11_opy_[bstack1l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩะ")]
          logger.info(bstack1ll1111l_opy_.format(bstack111ll_opy_))
          bstack111l1111_opy_ = CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪั")]
          if bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪา") in CONFIG:
            bstack111l1111_opy_ += bstack1l_opy_ (u"ࠩࠣࠫำ") + CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬิ")]
          if bstack111l1111_opy_!= bstack11l1l11_opy_[bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩี")]:
            logger.debug(bstack1lll1111l_opy_.format(bstack11l1l11_opy_[bstack1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪึ")], bstack111l1111_opy_))
          return [bstack11l1l11_opy_[bstack1l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩื")], bstack111ll_opy_]
    else:
      logger.warn(bstack11l1l_opy_)
  except Exception as e:
    logger.debug(bstack1111l111_opy_.format(str(e)))
  return [None, None]
def bstack1lll1ll1_opy_(url, bstack11ll1ll1_opy_=False):
  global CONFIG
  global bstack1l1l1111l_opy_
  if not bstack1l1l1111l_opy_:
    hostname = bstack1l111l1ll_opy_(url)
    is_private = bstack1lll1llll_opy_(hostname)
    if (bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ุࠫ") in CONFIG and not CONFIG[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰูࠬ")]) and (is_private or bstack11ll1ll1_opy_):
      bstack1l1l1111l_opy_ = hostname
def bstack1l111l1ll_opy_(url):
  return urlparse(url).hostname
def bstack1lll1llll_opy_(hostname):
  for bstack11ll11l_opy_ in bstack1l111l1l1_opy_:
    regex = re.compile(bstack11ll11l_opy_)
    if regex.match(hostname):
      return True
  return False