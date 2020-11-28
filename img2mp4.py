#
#イメージ(グラフ)を動画(mp4)にするスクリプト
#
import sys
import cv2
import datetime
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

FPS = 1 # フレーム/秒
SIZE = (640,480)

def main():
  #サンプルデータをランダムに生成
  # データ配列 x[5][1000]
  x = []
  x.append( 100 * np.random.rand(1000)      ) #  0～100までの乱数を1000個 作成する
  x.append(  50 * np.random.rand(1000)      ) #  0～ 50までの乱数を1000個 作成する
  x.append(  50 * np.random.rand(1000) + 50 ) # 50～100までの乱数を1000個 作成する
  x.append(  10 * np.random.rand(1000)      ) #  0～ 10までの乱数を1000個 作成する
  x.append(  30 * np.random.rand(1000) + 25 ) # 25～ 55までの乱数を1000個 作成する

  #上記データのグラフを作成し、その画像を g[] に保存
  g = [] #全グラフ画像の配列
  g.append( makeGraph('green' , x, 0) ) # 配列 x[0] のデータをグラフ化
  g.append( makeGraph('blue'  , x, 1) ) # 配列 x[1] のデータをグラフ化
  g.append( makeGraph('red'   , x, 2) ) # 配列 x[2] のデータをグラフ化
  g.append( makeGraph('yellow', x, 3) ) # 配列 x[3] のデータをグラフ化
  g.append( makeGraph('black' , x, 4) ) # 配列 x[4] のデータをグラフ化

  #動画ファイルを準備して、各グラフを１秒間出力する
  out = openMP4()
  for i in range(len(g)):
    out1sec(out, g[i])
  closeMP4(out)

  #おわり
  quit()


#動画ファイルをオープン
def openMP4():
  now = datetime.datetime.now()
  file = now.strftime('test_%Y%m%d_%H%M%S.mp4')

  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  out = cv2.VideoWriter(file, fourcc, FPS, SIZE)

  return(out)


#動画ファイルを閉じる
def closeMP4(out):
  out.release()


#静止画(グラフ)を動画ファイルに１秒間出力
def out1sec(out, im):
  for i in range(1):
    out.write(im)


#グラフを作る関数
def makeGraph(color, x, idx):
  # 画像のプロット先の準備
  fig = plt.figure()
  # ヒストグラムの描画
  plt.hist(x[idx], bins=100, color=color)
  plt.title("normal histogram blue") # グラフの指定
  plt.xlabel("x")                    # x方向のラベル
  plt.ylabel("y")                    # y方向のラベル
  plt.xlim(  0, 100)                 # グラフの表示範囲(x方向)
  plt.ylim(  0,  25)                 # グラフの表示範囲(y方向)
  #plt.grid()                        # グリッドを表示する

  #グラフ画像のサイズ確認
  #グラフのサイズを画面に出力(デバッグ用)
  # 現時点では、640x480になってないとまずい
  fig_w_px = int(fig.get_figwidth()  * fig.get_dpi())  
  fig_h_px = int(fig.get_figheight() * fig.get_dpi())
  #print(f'Fig size   {fig_w_px} x {fig_h_px} [px]')
  if( fig_w_px != SIZE[0] ) or (fig_h_px != SIZE[1] ) :
    print("Error fig size is not (640x480)");
    quit()

  # グラフをファイルに保存する
  #fig.savefig("img"+color+".png")

  #画像を描画し、openCV向けに画像を変換
  fig.canvas.draw()
  im = np.array(fig.canvas.renderer.buffer_rgba())
  im = cv2.cvtColor(im, cv2.COLOR_RGBA2BGR)
  return(im)


if __name__ == '__main__':
    main()
