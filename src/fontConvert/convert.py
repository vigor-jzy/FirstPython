from langconv import *
def Traditional2Simplified(sentence):
  '''
  将sentence中的繁体字转为简体字
  :param sentence: 待转换的句子
  :return: 将句子中繁体字转换为简体字之后的句子
  '''
  sentence = Converter('zh-hans').convert(sentence)
  return sentence
if __name__=="__main__":
  traditional_sentence = '憂郁的臺灣烏龜'
  with open("1.ass", "r", encoding="utf-8") as f:
    # print(f.read())
    simplified_sentence = Traditional2Simplified(f.read())
    print(simplified_sentence)