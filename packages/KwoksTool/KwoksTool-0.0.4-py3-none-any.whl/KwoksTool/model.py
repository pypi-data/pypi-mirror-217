import pandas as pd
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import email
import imaplib
import numpy as np
import re
from email.header import decode_header
import execjs
import json
import mimetypes
import smtplib   # 发送邮件模块
from email import encoders
from email.mime.multipart import MIMEMultipart    # 使用MIMEMultipart来标示这个邮件是多个部分组成的
from email.mime.base import MIMEBase
from email.mime.text import MIMEText   # 定义邮件内容
import  datetime
from email.utils import formataddr
import os.path
import sys
from zipfile import ZipFile
import zipfile
import os
import tushare as ts
def GetProbMatrix(df):
    name = []
    for son in df:
        if son not in name:
            name.append(son)
    result = []
    name = np.sort(name)
    for i in range(0, len(name)):  # 遍历行
        result.append([])
        for ii in range(0, len(name)):  # 遍历列
            result[i].append(0)
            # input(result)
            for iii in range(1, len(df)):
                if df[iii - 1] == name[i] and df[iii] == name[ii]:
                    result[i][ii] = result[i][ii] + 1
        sum = np.sum(result[i])
        for iiii in range(len(result[i])):
            result[i][iiii] = result[i][iiii] / sum
        # print('sum is ',np.sum(result[i]),'序列',result[i],'\n')
    result = np.array(result)
    return result
def ToMat(df):
    wide = df.shape[1]
    high = df.shape[0]
    df = df.values
    result = []
    size = []
    for i in range(0, high):
        for ii in range(0, wide):
            result.append([[df[i][ii]]])
        size.append(wide)
    back = [np.concatenate(result), size]
    return back