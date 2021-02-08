import numpy as np
from scipy.fftpack import dct, idct
import matplotlib.image
import matplotlib.pyplot as plt
from PIL import Image

# 이미지 불러오는 함수 -> width와 height로 이미지 사이즈를 강제 조정해서 불러온다.
def readimage(path,width,height,i):
        img = Image.open(path)
        img_re = img.resize((width,height))
        img_re.save(f'testimg{i}.png')
        im_matrix = np.array(img_re)
        return im_matrix

# 구현 필요! 현재는 라이브러리 쓴거예요
def dct2(block):
    A = dct(dct(block.T, norm='ortho').T, norm='ortho')
    num = np.abs(A.flatten())
    num.sort()
    np.place(A, abs(A) < num[-16], 0)
    return A
    
# 구현 필요! 현재는 라이브러리 쓴거예요
def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')
def recover(matrix,i) :
    global p
    img_recover = Image.fromarray(matrix,"RGB")
    img_recover.save(f'recoverimg{i}.png')
    img_recover.show()
testimg = []


p = 6
width=160
height=320


## testimg.append(readimage(f'이미지 이름 넣어주세요',160,320,i))
testimg.append(readimage(f'test/test{p}.jpeg',width,height,p))


## Block에는 이런구조로 들어갈거예요![1번블록: [ [16*16 Red block],[16*16 Green block],[16*16 Blue block] ], 2번블록 : ~~~~~~, 3번 블록: ]
## 
block = []
## Rblock, Gblock, Bblock 에는 각각의 색깔에 대한 블록들이 16 * 16 크기로 들어가있어요!
## rblock[0] => 첫번째 red block
## rblock[0][14][15] => 첫번째 redblock의 (16, 15) 좌표!
rblock = []
gblock = []
bblock = []


for element in testimg :
    for i in range(0,int(len(element)/16)) :
        for j in range(0,int(len(element[0])/16)) :
            rblock.append(element[16*i:16*i+16,16*j:16*j+16,0].copy())
            gblock.append(element[16*i:16*i+16,16*j:16*j+16,1].copy())
            bblock.append(element[16*i:16*i+16,16*j:16*j+16,2].copy())
    block.append([rblock, gblock, bblock])




widthBlockNum = int(len(testimg[0][0])/16)
heightBlockNum = int(len(testimg[0])/16)

for i in range (0,len(rblock)) :
    rblock[i] = idct2(dct2(rblock[i])).astype(int)
    gblock[i] = idct2(dct2(gblock[i])).astype(int)
    bblock[i] = idct2(dct2(bblock[i])).astype(int)

## rfinal에는 RGB로 나눈 이미지가 들어가 있습니다.
## final에는 RGB를 합쳐서 복원한 행렬이 들어가 있습니다.
for i in range(0,heightBlockNum) :
    tmp = rblock[widthBlockNum * i]
    tmp2 = gblock[widthBlockNum * i]
    tmp3 = bblock[widthBlockNum * i]
    for j in range(1,widthBlockNum):
        tmp = np.hstack((tmp,rblock[widthBlockNum*i + j]))
        tmp2 = np.hstack((tmp2,gblock[widthBlockNum*i + j]))
        tmp3 = np.hstack((tmp3,bblock[widthBlockNum*i + j]))
    if i == 0 :
        rfinal = tmp
        gfinal = tmp2
        bfinal = tmp3
    else :
        rfinal = np.vstack((rfinal,tmp))
        gfinal = np.vstack((gfinal,tmp2))
        bfinal = np.vstack((bfinal,tmp3))

final = []
for j in range (0,len(testimg[0])):
    for i in range (0,len(testimg[0][0])) :
        final.append([rfinal[j][i],gfinal[j][i],bfinal[j][i]])


# 원래사진 5,5 와 다시 합친 5,5 테스트
print(testimg[0][5][5], " VS ",rfinal[5][5], " ",gfinal[5][5]," ",bfinal[5][5])

im_m = np.array(final, dtype='uint8')

im_reshape = np.reshape(im_m,(len(testimg[0]),len(testimg[0][0]),3))
recover(im_reshape, p)
