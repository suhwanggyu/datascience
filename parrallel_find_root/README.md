Bisection and Newton-Raphson method
====================================================

이 프로젝트는 한양대학교 2020-2 이상화 교수님의 수치해석 과제에서 제시한 Bisection&Newton method의 구현을 심화시킨 Parrallel & Hybrid version입니다. 하단의 논문의 제안을 확장하여, 모든 구간에 대한 2번의 Bisection을 통해 초기값을 찾고, 해당 지점에서 Newton-Raphson을 수행합니다.

#### 문서
[PDF](./report.pdf)

Execution
---------
| 값 | 의미 | Format
|---|:---:|:---:|
| `-e` | equition | `"[계수]"`
| `-p` | parrallel | `Y` or `N`
| `-m` | method | `newton` or `hybrid` or `bisection`



```
python main.py -m bisection -p Y -e "[-23.4824832, 24.161472, 15.85272, -22.4, 5]"
```

<br />
다음 논문에서 참고되었습니다.  

Parallel Hybrid Algorithm of Bisection and Newton-Raphson Methods to Find Non-Linear Equations Roots – [Khalid Ali Hussein1 ,Abed Ali H. Altaee2 ,Haider K. Hoomod3]  

Source : https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1043.5769&rep=rep1&type=pdf