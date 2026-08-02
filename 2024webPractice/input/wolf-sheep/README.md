## Init Env

1. install python3 (on Mac)
	* brew install pyenv
	* pyenv install 3.9.6 
1. install virtual env
	* mkdir -p $HOME/github
	* virtualenv -p $HOME/.pyenv/versions/3.9.6/bin/python $HOME/github/v3.9.6
	* source $HOME/github/v3.9.6/bin/activate
1. get source code
	* git clone git@github.com:tiger_class.git
	* cd tiger_class && git checkout wolf_leadership
1. install dependencies
	* cd wolf-sheep && pip install -r requirements.txt
1. run code
	* python wolf-sheep.py
* check chase.log(s)

## Movement formula

TBD

---
## Todo
### improve performance
1. replace grid + kdtree with pdist() directly

### imporve logging
1. output config, steps and result to file, reply steps
1. when repel happends, output the distance in log
1. using loguru, output 3 files: config.yml, steps.log, events.log
---
# Formula

## 每个动物的 取向速度 $speed_{align}$
* ${\displaystyle speed_{align} = {\frac \alpha n } \sum _{i=1}^{n} credit_i \times speed_i }$
* 对于每个物种, 其取向速度是 $r \le alignment\_radius$ 所有同物种动物（共n个）speed 平均值。$credit_i$ 是第i个动物的信用权重，对于羊，一直为1，对于狼，随着其领导下抓获的羊增加而增加$\omega$倍

## 每个动物的 排斥速度 $speed_{repel}$

* ${\displaystyle speed_{repel} = { \beta \sum_{i=1}^{n} \frac{-1}{ distance_i^2}}}$
* 对于每个动物，其排斥速度 是 $r \le repl\_raius$ 内所有同物种动物(n个) 与距离平方反比作用力 乘以 $\beta$ 

## 羊对狼的吸引里，狼对羊的排斥力 $speed_{chase}$

* ${\displaystyle speed_{chase} = { direction \times  \gamma \sum_{i=1}^{n} \frac{1}{ distance_i^2}}}$
* 与排斥力算法相同，但是距离是 $r \le sight\_radius$, 另外羊对狼，direction = 1 正向吸引，狼对羊 direction = -1 反向排斥

## 最终综合速度

* ${speed_{next} = speed_{init} \times NORMAL(speed_{current} + speed_{align} + speed_{repel} + speed_{chase})}$
* 最终速度 是加和 当前速度，取向速度，排斥速度，追逐速度，然后归一化，指示最终速度方向，大小还是 初始化速度. 注意不同的狼初始化速度不同

--- 
sripts for fomula:

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.13/dist/katex.min.css" integrity="sha384-RZU/ijkSsFbcmivfdRBQDtwuwVqK7GMOw6IMvKyeWL2K5UAlyp6WonmB8m7Jd0Hn" crossorigin="anonymous">

    <!-- The loading of KaTeX is deferred to speed up page rendering -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.13.13/dist/katex.min.js" integrity="sha384-pK1WpvzWVBQiP0/GjnvRxV4mOb0oxFuyRxJlk6vVw146n3egcN5C925NCP7a7BY8" crossorigin="anonymous"></script>

    <!-- To automatically render math in text elements, include the auto-render extension: -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.13.13/dist/contrib/auto-render.min.js" integrity="sha384-vZTG03m+2yp6N6BNi5iM4rW4oIwk5DfcNdFfxkk9ZWpDriOkXX8voJBFrAO7MpVl" crossorigin="anonymous"
        onload="renderMathInElement(document.body);"></script>

