#!/usr/bin/env python3
import argparse, base64, hashlib, io, json, math, os, sys, time, zipfile, zlib
from pathlib import Path
import numpy as np
import pandas as pd
import requests
from pyproj import Transformer

ROWS=335; COLS=781; N=ROWS*COLS
HEX_W=57735.0269189626
HEX_H=50000.0
R=HEX_W/2.0
X_STEP=HEX_W*0.75
BASE_LEFT=-16920565.0448
BASE_TOP=8315130.3484
X0=BASE_LEFT+R
Y0=BASE_TOP-HEX_H/2.0
LAND_BITS_B64='eNrtXX2oHcd1n7379PaaPr99jlP6ksramzrULYXmFdNYqeW3N0mL8kcghhQSSohekhanUOKXhNZyrGhHSPAMCcgtpXXBzTP0n0LTVv203HzcFXIrF5w+gSlJ00R3bTmW2th6q0jO3ae7d6bzsR8zuzOzYyI1xPaCjX3v783O+Z0z55w5Z3YvAP+Pl2ONHDrX985LdMzeDRCpD34818Ng7rqP+fYbo/RXQdFwyRI4B5Z+jNb52ruG4I3rjet1YULwdc1op5Oz96s3IvQtKz4bvKoo/6Mo/J0/0jx1kerVX72fFAvtg9fYBW8A8jV3DV5zEvWu/8KwJWnpx+oVeq9CojdyxOu6OIY3wKkMXg8Mw58QOuasxXGuv+i2i3XZmqR563v7tmlB7M1ZOqDE61mSlO2yFT0/tmaJDNdsvfSek31LW9z1y7a+1wstRYenxrZ29Nz9lsi1LLBVe+bZrkrk2o6JLMcEj2LbMZ+KbJfb5IDtNK/8kq3Fz3xLZIJsp5lG1hoKbZG5tdZzW4HWsK0uU2tkjh1rpK1AOLzuyBhba70SvcstZ69W9KWbu1cbsySIu5WPIy5XJxJykrJuBmKOxAQ512UfPqMK42DeHOj4bVOCHHldJFH/gQgS325OgxFDEtw9eWRGYuzsZdP0Y6OlzEOCXCCTxUT7F43pOhmN5OxsmmDFRLtDkB+ARynQ7BkhpSc8tdONXCMzHH0B8+sus4fPcXUFpj3HMpNljKcUGXbRifFxPqaZToCFKzYsk16MI35rdumBjzgxHgmD6pEPEzqnVsjfZnZJr2kHckCIn04ohin+83rkW0TiMdbb57DPjQhvdhIq02kYc8mFElI/5hcJneTa7kY+xdZPfem9yMetkXeylWaBhMu2yHhBJl6/kAbzBfGdyBVXJl7v7x92RGSY6k3pJRCLt47foUX+gYiMANQ6enh3ZceMoUTraJNApJNm/1qkL9BJ7px6hpyzppOgMqaiN6scvEgnofKQr9ujIQdK6xdp1Y4Fm4torNPNE0YgGQnWXiAVGiWRIhMFSrQGkgYVSREFpXqkD85FokBaA8k9cFjUkN4r5S787+1aoEzvF7ATT8YENeHIPNIjBd9JtI7P6PxCTOh88mt8SLooo1g3JqHzxCGUl3TGgTZZJnQe/FBNfOJqs1BC52Nb08qS1kG+5Wrp/Pr2rEIuATR2tHRuT8SAqV3u2IGTqeiP9EjwAh6PK0si2kwdHZ0vSv4IeokaeTaEf4cnE9EfJTo6450xjkpLovvnpKehcz1/BW/uFIuIlhnW1eMi72A+++60tDk604z8/Y6noHP3Np7NCmRMb7xKFp1i34mdxX/CD352GzEkSyY9avduOz0F9+P70dMF8UskP49Zatm6exLBcPTAQwcRJ56maUOWs3lt64y3qjjogd0syYpVgSYNLo5J9C/49BboR06iyq5SP51QGBfeY/mvk6uCbO5dwyFGCLEZeF6RKStCPDqazwgmHGc0V+PEq5H4SJ7/zhRvhjmeHr8NevOg9M+tfcHgMNreGl3Y4J7mqAOgOmWKo3sPY2LyF05z1/kFpwo4DUKT8FGMX97GexFl8PlT761u3kRmwWOYqPyhZf5V7AKANUj/Pyg7wTPM4PsJqKbZNJHce5HyfusLVIT43Qmog0MT6U6pehZ3plSg3krB+6yNxEce/CFZbRvjHWoSb1/q1cGBIZdqOuODeBzh/RO+PYFOHRedBp3Dr+IthMOPsW/eBAEca5DhsfGE7CCCbzE9w18Ha8+r09okOLsVHRljwhW1sv4+MNAkwKn/vSdWCS8bE27jQZ1mNGwp23jnTkCQRPNUoLlAiLUNOo/+6yGPMHgZMQGIMnPNmOhtv3GV+HX8FcwSH4Ks6DzcIH5I3Cf58vu4dHIlnaHMEonscESRE/75GmB3H7GoLC3Op0OYhvTLKV+JK0DMGcUV/0IAMxbcd/wSiSZCgldP4BV/+EOWAdWeTZNczrzPXHMB9chOZTL8GrN9xSgvdwYz97YcwH+vHMYcU1HUTkQT5HyE0PZU5YTmK2XO5L3fWfy+USg6S4cpM2pvK05Gn3woYN7FKQveqZwF429y5NXwtw4Tei7hqbCHly/vTq714K00oI/Le0CuTOnuq3yA4xfIfXO8XSmuXhvltcUmhjf+HhGfPq71BnHrYuxjd+EcTSgnlWN5vI1kdoudXZjsSAWjheImiRPLQ1Fy+utOKjh/eLaFZGOmUfbuP6dsltOcW3pfofImMnx/skh5KU3mL3sKiXhpcP784hJif9YvY2PzuuCw0uC333VHLq3CpIVkZU68/8V9b5KqCk5rTLa6If6Hh/xYjnvimONqnjH+sxn1CuLKgrLWK+Qz2MFXJOfbvPuICZFGH529m/7PzdKYkuDHOTJ8KIhzHEVue57F4rhyepOKm28+6z+Fx18bOWqJyMK/Jf4CQ279r3OZqPl+qcBVXZ8l/yysASou2v/KkcskTxND/kkcCXWJ+8jEKRJPH1ojGnpwUUBekkodlHSPivng5ynyiyISNYsiFBnja8EtJFV5jxjLRCYZQbQsk0Qf3egjfI9UopEkpwLElJBReN88fvnue4GOeL8omeabH7rDP4/fMdAhpxVye/u0n+Gf6UtIQaDLpQD4wivf9zJ866JuzMvV5KfZky7KnZ6UOP5Xuxx0DO/kM7cVyVC7zBLj1Ryfakay7yjKLM9He3KcNPO8WFGJuzryUJRhX07Ik1l183J3OpiNXXwA4Q2nUaWu1lvZlVyZbZNNLcbPAQ2yWoYfPjeBI+8kzppFXYkjqqF3je+GW05cOOe2mz9QFAYB+OqV25ItEI8iDbKSfPidyeIJEgy2G3kzaqUWK5c+51Hkpq9ERofqu0yedEgqkZxpJm/NyH5vFJ7rkZ1V0qx8FA6u/hRO933Kobugs24ja24mQB8/ePwJZSWYzXMmpDWfyY8/qzqwBVtl2gV05WV1Lb+ZqvTQ//yauo3RSD8ecfDBuw3I2r5iGP3Lorrq38joBjD4jjXyb1x11V8WHYLYe8KxQYK5+OhUve1uiD4Acfx5A1K6XbyqJ142xPVQj5QlOOGr2y3tzc5jvmbM1i7zG16iHrO5x4Uveor9OR2zVZKePqvq9ip6THAnUpViE8UGGz2hquKk7ZLJGvqmEtkuF51Ql2IVdc9HTUVbweYAeMlY/68YIv9csELSa2qq1Usz38GWncyzqiKG8jqIsGVD/h9tpwk2MbbrSsOXbae5dsFmmjRMrk1teKfa/taODZsMiSz6wpBV420FAv9cmlznGZzvYssOMqHT9oTBxBo5tdQliGclSV3nZRJkewZkvdT6sAt50na1gXPWol8qBRp001kg7+1S0dRW9Isz23MDLyFb0T9nLfpXrLS+RLR+zto+LtkujRMTW2Q2tSUpn9mShJAtSZHoP0zzgCN8k0ga2yqpl8YY73LqhGSddjs0yG18yq3vfeioVg/ZBMcVcgEa2qPZNEzk7Ew3Jtrx0jrDyk1I5BwU845tHRJGCOyTU0MdcnQXqL4a5IbGdLL506AStm/qzqZboCKpzHU1JN2xq94HpyZkfitrkEhbHE0H6CYBiQxIiOfqR1qgqdF/NurVoSUxIdNRu06hRuabkhM3INE72ps7NRLfUfr3+vxCpBad6eedAF4IYuOBhCJrDGlKmmhPt3Aks0qfnmTLNI2FQgg2p9Sj3dvceCQAhTQAZrQ8ecR8uoTPKacMVVVjzQaEGPFSf5XuRGZG0WM2+5UeReZG0Xm/et/AgThEZblLKTo/wBY9skzoREaSGJ0w/NRCUp7/0ZHE6ByG4XyKNzqQVM6nse9m+LwFnTHaIPp5zoiERT/2WReFWTedEKDLhEQznXFRRCYoD3eQxKzzcI7Dyj7ud/XWCb5EHHZiFr044PYnhMPUfP4HcTnJTmLJLFBhncQ2o7o84xvoJH4rAGbRy40fGeioWevFaYqY3Dw2i14cr0xxOEi6kMwp0Gmatc6PV0YAC8hJqKUzpu5IOAij2e8HtP3GNt6ow8/5tJuZ4mnjeIuazpw6LqHKGaktiTZOf5eYnFDoC9Uk3UIGy6joCTYaSIb7IKGuY+NQZlY7ihZIHvOfGJ+5J+9Ahj1wlfps1zcfpyJ0ugCHl6j5iOekVAvzuBPjTbIrdIUe0RGkovOMcwLTKXrwGeNxrhSfJ0vuMDPe2IjM8KcBjkKMz7uD2HiYLMfLkB2bTJ1eYhyT0EmG+lOMLztuKo8ZBw06KYA4wxQ6mVyDR0GDTgKYpThKYqk7F7IlKNG5BZDvEa+wnvQQrttz0XwmW2mMz4BLGy7BpOvc5KPC8INGzSHBH4T4FOC1Wn5bpD7HmOJb4hk4Rj7MXD6m2NcQ7TTDb07o5HH4e8WYYw0SRXMp626Hc42mbHOVoNDJP0ZTvqCn6iKG0mLPL1PKCbLdcxOUShd7lCdcJ4nYeymuO4VQRDLkq5yQRDEmFnxnvHlXpkdGQigiS6NAVqa0PW0jie9Mo/upZUQOzBVjBkIoysKX+B8rp+kLvvOlotUltMcEzXsinRFPfJz6yIBiOVE6R6+wIVDj+GaLJOKHP8QghwA2k+RC/EeIHWKHYs+rpXcSiiD+Np2nP+9gI0nVgcQPvi82kkRZvMJEd9+jRHqVfYRERUwg5+eUxLuV6CSsRYzHv15SIp0KScJaSEWNgptSBUcCSR44F9LPngwaZ3G5VkMxFG0xMi4GjtmSyDwY0nv6AMhNJBE64fkZsyNfqXZHoDM+j6jOkC+pfbsZZ2mo/H12PoksPGxY7bTunRwi/sWHaqQPBDrXmUAxdhKDhgiDHtjLkGkEUpNA9HGIL5NF88Cu/C6JpMLZhsK20gFXH0B44uehQNJm6Wx8od1Be2X07mJGR4JmYfVOLToxAET//uhoU0QeQA3Xzbqd9K+Px/g+kaTC098muPgArFBt7E/wnfFlwS3MmJI8wcX74FuMtoQspyvFzmikiBs5+StmlLdQOi9EmiXESHLBNfrH/YyQdKWWnE+BSz7H994OH9PPgjSsliYs4ozUayn29DRqohIZJa34kpA5D9h9vJwNVSyIi62YRek8y00GC8hFos4L5B6uGAfLRM6V3Sdx5CiUE5APDPnKPcWQhYlMtqmr9eV22B3rAtIVzW7mykh3N39uhBmxh7DmiQsyRWcPXYXbOON2z6hF7USVIOGWuGagYO2+nHtF8TdENcMqA2mknyQvXn++er6DrU9NAkY2DyvPi6sMCrGg0TP0Fw4KsYJuJyJV5k1G8ObpGbLacPPq/EnQ6Nq5DpJKAEW38+ZGRklIOgLEUFWO6TWfryPIIZd2OmHrKypyNXoEqZH0RgNucxlGbAocGSjS45DHlTArCOdIV5EeB32m76B0ctzsHEV67PN00y2jCzOO4uaixSPsMeTMKccM89o0xEkQt8VMIqoiVnSN33wotx7pYudmVjvjtPQwGZaR1CuSic3trR/zYNMcgPIvYLnYGUlBFbJoMcIrRgnlxc5uu+FVRxVyflO65RVsPpsF4AcsmtHgxqzZRcVNE8nmM+TH9frJCh9X7/jr6+tkLXKDI/EtSgt3U+74fQnpZpeKfRgO6JhhUnADJZXC72Mn4zL/SsxVT/9VpTEC8gouyfnFlI9JXGMxzYloT3EWAX5zfE/GbkxF9+rtfN1KJOHvcBUjGRIUN280pmneWXssakVR+chlFjX37LBGUodNNrFc4sYjMeQWawKS6i9RlxZIorTOTpOyYpafUkerbouQRCm5UrljnxrkPk1FGoN9eWGTPB7pGhHkm8OoWpge0nd5iMJweV+yovQNUKJqWK9HKpauFUYSpbjes0V0Y6l50pQkSmelZCLSI918VhMv+62h7OPFvDTM9c0ojMVsM9Q/5Bwz9y8itQ0gHMYzIXdEWt7JehDDlC+tRSiLznRThqkNfX8r55lHFVv1/XGEbz0spoZKVcZ86d+EO5+zHHLkU+M6SBq6cMR3/tvY5klHGoouY2wuZPGMjoSiy9NuJCNpK1dnj2372I9skbcT/USdTxDSHOAPrZ41pMgYW5IUxVaPg1I6fyAUU4wkBdcY5kzHQ54EeTwXnq71TSRtIJKmbBcJkB5JLOkv7B4xjakfmtZVB8dgcyyHnZVbDM9EZ8pSqXGX2jNc9B+2u5B51X94uYN5VGbNxXq/2UBnmY9PzWPCYvNg8XhtsVWqLNk30JnYPV5L6FyTdnZOJ52dazjnuUSl98hE5yWrecLm9kZ7+xad2hVHDO7ITDwSTdxnX3loiCCHBPC3kqPtqUmKYKN+Rgj9BSVJxbZ22iU8kkORQfFIbGWZkLDcA7JHObg9B1o680ZZLtRZZ7vi5Gisk0X2UScylSO7ERky4keoKxrmBZ0j1OW+JTpNToTSmWD140EtktxMtDiyUO/WLWGnUeoDcFVjx5TOCVfQjK0N9ZPAWbn/rKKMT5/cUlsnbLKufvhdtM7tknVfPWbDOgOD70ylarUhR6zpHM8Mh0Jb1hkakBVJow4v27BOzxDZod07IbIijZ9ZeFlfeiLNN4Uiumve7M6UWLUPh1c6wwalM+Gbh46wQRd7WnenDMEgFUoFXSSFS3ZJIlnsy3a5Clnsx6yMky72Y3bKJASetxqT0vlckdFsdyGHmeiOfQOdw8xqnpROJM/zUE8XimRkqHtzJ6Hzj7FNaJdCUYkc6EJRihtFzqGd74wM1plLb6rRnvMjdCKr1Z6Ve3apd+yo6XykVSzXIP241chRvZ2A0vlUq9emQbppC5k5ajrTVjMlu11HZxOqGjMVD76Urt5NTxvorHO12xP35IaqinlbM1twEy/1VW5hodlLcmMv8x1F/cVrjQnCNOgpkG4z+XJgpHjXHD0zkTQa0Q7EWaRQ0Var3Uf+XPHCrQR/ooV0IVYcy43xnU0VTRwyJlaoaFlu911h81QhowWJpJDVGw8qkLk/LxEfkL0cAOuJAun1JIsntjr2qlNb0to4Irf7HF4XJSlQM4/HsKwwh5zLlDmGiy0dwXCtpLNCUtBLZ0rEQklnWL3lix21i/bxF9AsVAd4S/NL/YrO0+zfq7wI3i/PpkKvQvYLOlnlIDrgF8/flHXHtPSlmdsDfPHwzcRxj5c7e/ukc3OAreuYH54bJ9yIoU+cJ3T2lGX2cr6HWUGNaWmHhiRHFlmoah5m3e7HeWnwQvn5Cn11CB+y8qUBQ9Ixgz0PVJEI8ZeXACREsUXW7aZT9I6O6r4C94qJeBjBY/VJ9tGRaeWNSY5ZIqsn/F3WeaT6ZI9TF4/UYy/j8tQCJXV9knUknPLER1ZMU0TCIk8E8Cvl54iXhqEYRvbS/+dptwunlegcKT3Cvcy73biYp1e1PBZ4kl8HnEV+zGBUIN2qtn8z571GzjM6afYXAVhW6kmOOfS4QLV2HUbnI7MIf5Z881NVgALlCwEbRdyzGO/PKutmTQuHix42kCmNxmICE0CnIXpR7n2Uhg/x9LcHmqIXyL0U6dHX2RSacdcK0eWjTyEZM6RjwrC4OXZWuNYlgc7iXwXL9CBMnx5i5AbksgdKUSN5uBj1wW4yn9UiAqwxX9dXiE4d+m5Q/0jCUkKPOc4rRKdl6N3lgzDXfNBLzzpMI2kzwSuQbLhhFsRghVaBdzW0Xp5zXCzrrzPyVX9IFkKPH8Jymsi3VjfYzyj/BDEQ2G4je1yaZTq5vZ8ifgaShNABebuN7PHE8Laqpb+C77uFG5KEvDYqLJ/PlaZ+Cz6xeNhuOIe8MnOV6/w0kWE+BMWpMrnhHK4wMvcyQ4PPwV3gfFSwKaehrH1HkB95P11j8HufAODTq6B4s44j2xy5/QkXPMDS3ceffwuI+58cFkfaGsiIeeif5f872A2GC0uDIuw1Unky5kHnGS46/Pk5sLLrTZCnWo1jgdsEuW++WEWxH1LTfJqHKOk9vgk+TyzkS/uLt+bCOAALPVAGHk9CPkeQe/xy8lfJSndAGcdvl/KAqz6Ax3H50EF2M42rZXTuS8g0APBIpbeUvgFgWLzDIhJTpizIyJj1m+LI6h307i1O8x1gC6EnIEk8rKRcYVGDt3FGD0oZA+vg5Y1GTXkSRMirc+8qRdYPhYCH50B1Ri84WSOR+7Q3AOKT5ey1M+VuUqjHXHP6fyU3Xbyl+kl1f0/9xWohnCN1SMoE2xWMfo+qlwJniq6QYi/igmFRF4kS6ePmNXCr9xRFa5omF/8EgrnqgE1fRDb2gMNhD/QuKradg1ZKRldortycN5GxgDQ/wJbuqt9kIGf0zaw921Mj5W+cVjpaab3jsdbc7cHu14lS8V74GIiPdNUl+GIl2dsxE7InJCZLcVe3hbMEKvM0Ax8/BMr3Z3Q9jBgB8Sl9w7O37E3AcTXNgaY2QAWizjyxmCYJEAvFE1arXUhqQMiCd3ZiLVaVL4aKYwLFlqG5vNpjFvuVzuejq+pmk/elNhLarAyqnWmKu19yzLvqWdfrc0GVeWZmgYbV0YPisB7Q/uTL3HyRdIPHzhfmsVuN/HB9WKQ8L2TUZxrycBCImy2litjb/lPOUWJcR/x3Afgr11KT+wL8eAl/8f0+swfxix0bKBPcOkw07u5rQkBPPc9qP2S4nqmRidlCjgnvdOkwpnpyu424oaCXRSNyIIhhFmil/h6afeKy7B0N10L9n3vNSEETZoHEuZlX8bocFO0ESoDtZS+Q/c+/3YAfberQpWAUMbBF2v/ynfUPQ8Auj1yJkXR55OqnZzLraa7aAuOuSFgFvM7fIhm8p/iPZzvfHvBeSw2xTGB3kf2DjtVe2OWyzZh2FgwBuAE/tPua+5W9D19/aeDSb1oi37YLvHG9cb2erjXrH0yzD9Q34KdMh9a//TqwHrPljf8PTbARog=='

SOURCES=[
  ('NCAR_GeoCAT','https://raw.githubusercontent.com/NCAR/geocat-datafiles/ad7bedcc2a14a37f08da1a5ce3f0859ad9e51023/binary_files/ETOPO5.DAT'),
  ('NOAA_NGDC','https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO5/TOPO/ETOPO5/ETOPO5.DAT'),
]
NE_URL='https://naturalearth.s3.amazonaws.com/10m_physical/ne_10m_land.zip'
EXPECTED_SIZE=18662400


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
    return h.hexdigest()


def land_mask_hex():
    raw=zlib.decompress(base64.b64decode(LAND_BITS_B64))
    bits=np.unpackbits(np.frombuffer(raw,dtype=np.uint8),bitorder='little')[:N].astype(bool)
    assert bits.sum()==68048
    return bits


def download_etopo(out):
    out=Path(out)
    if out.exists() and out.stat().st_size==EXPECTED_SIZE: return 'existing'
    for name,url in SOURCES:
        print('DOWNLOAD',name,url,flush=True)
        try:
            with requests.get(url,stream=True,timeout=(30,300),headers={'User-Agent':'civ-map-stage1b/1.0'}) as r:
                r.raise_for_status()
                tmp=out.with_suffix('.part')
                n=0
                with open(tmp,'wb') as f:
                    for ch in r.iter_content(1024*1024):
                        if ch:
                            f.write(ch); n+=len(ch)
                if n!=EXPECTED_SIZE:
                    raise RuntimeError(f'bad size {n} expected {EXPECTED_SIZE}')
                tmp.replace(out)
                print('DOWNLOADED',name,n,sha256(out),flush=True)
                return name
        except Exception as e:
            print('DOWNLOAD_FAIL',name,repr(e),flush=True)
    raise RuntimeError('all ETOPO5 download sources failed')


def download_ne(work):
    import geopandas as gpd
    from rasterio.features import rasterize
    from rasterio.transform import from_origin
    work=Path(work); zpath=work/'ne_10m_land.zip'; shpdir=work/'ne_10m_land'
    if not zpath.exists():
        r=requests.get(NE_URL,timeout=(30,300)); r.raise_for_status(); zpath.write_bytes(r.content)
    if not shpdir.exists():
        shpdir.mkdir(parents=True)
        with zipfile.ZipFile(zpath) as z: z.extractall(shpdir)
    shp=shpdir/'ne_10m_land.shp'
    land=gpd.read_file(shp).to_crs(4326)
    # ETOPO5 point centers after longitude roll: -180..179:55, lat 90..-89:55
    res=1/12
    transform=from_origin(-180-res/2,90+res/2,res,res)
    shapes=((g,1) for g in land.geometry if g is not None and not g.is_empty)
    mask=rasterize(shapes,out_shape=(2160,4320),transform=transform,fill=0,dtype='uint8',all_touched=False)
    return mask.astype(bool)


def cube_round(qf,rf):
    # axial flat-top -> cube round, vectorized
    xf=qf; zf=rf; yf=-xf-zf
    rx=np.rint(xf); ry=np.rint(yf); rz=np.rint(zf)
    dx=np.abs(rx-xf); dy=np.abs(ry-yf); dz=np.abs(rz-zf)
    mx=(dx>dy)&(dx>dz)
    my=(~mx)&(dy>dz)
    mz=(~mx)&(~my)
    rx[mx]=-ry[mx]-rz[mx]
    ry[my]=-rx[my]-rz[my]
    rz[mz]=-rx[mz]-ry[mz]
    return rx.astype(np.int32),rz.astype(np.int32)


def xy_to_id(x,y):
    xl=x-X0
    yd=Y0-y
    qf=(2.0/3.0*xl)/R
    rf=(-1.0/3.0*xl + math.sqrt(3)/3.0*yd)/R
    q,r=cube_round(qf,rf)
    row=r + np.floor_divide(q,2)
    good=(q>=0)&(q<COLS)&(row>=0)&(row<ROWS)
    ids=np.full(q.shape,-1,dtype=np.int32)
    ids[good]=q[good]*ROWS+row[good]+1
    return ids


def group_stats(ids, vals, prefix, all_land_ids):
    good=np.isfinite(vals)&(ids>0)
    ids=ids[good].astype(np.int32); vals=vals[good].astype(np.float32)
    order=np.argsort(ids,kind='mergesort'); ids=ids[order]; vals=vals[order]
    u,starts,counts=np.unique(ids,return_index=True,return_counts=True)
    pos={int(v):i for i,v in enumerate(all_land_ids)}
    out={f'{prefix}_N':np.zeros(len(all_land_ids),dtype=np.int32),
         f'{prefix}_MIN':np.full(len(all_land_ids),np.nan,np.float32),
         f'{prefix}_P10':np.full(len(all_land_ids),np.nan,np.float32),
         f'{prefix}_MEAN':np.full(len(all_land_ids),np.nan,np.float32),
         f'{prefix}_MED':np.full(len(all_land_ids),np.nan,np.float32),
         f'{prefix}_P90':np.full(len(all_land_ids),np.nan,np.float32),
         f'{prefix}_MAX':np.full(len(all_land_ids),np.nan,np.float32)}
    for uid,s,c in zip(u,starts,counts):
        j=pos.get(int(uid));
        if j is None: continue
        a=vals[s:s+c]
        q10,q50,q90=np.quantile(a,[.1,.5,.9])
        out[f'{prefix}_N'][j]=c
        out[f'{prefix}_MIN'][j]=a.min(); out[f'{prefix}_P10'][j]=q10
        out[f'{prefix}_MEAN'][j]=a.mean(); out[f'{prefix}_MED'][j]=q50
        out[f'{prefix}_P90'][j]=q90; out[f'{prefix}_MAX'][j]=a.max()
    return out


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--work',default='stage1b_work'); ap.add_argument('--out',default='CIV_GAME_MAP_STAGE1B_ETOPO5_5MIN_STATS.csv')
    a=ap.parse_args(); work=Path(a.work); work.mkdir(parents=True,exist_ok=True)
    src=download_etopo(work/'ETOPO5.DAT')
    data=np.fromfile(work/'ETOPO5.DAT',dtype='>i2').reshape(2160,4320)
    # Source is 0E..359:55. Roll to -180..179:55 for land masking/projection.
    z=np.roll(data,2160,axis=1).astype(np.float32)
    landpix=download_ne(work)
    print('LAND_PIXELS',int(landpix.sum()),'TOTAL',landpix.size,flush=True)
    # Land-only slope: central difference, require four land neighbors to avoid bathymetry contamination.
    res=1/12
    lons=-180+np.arange(4320,dtype=np.float64)*res
    transformer=Transformer.from_crs(4326,8857,always_xy=True)
    hmask=land_mask_hex(); all_land_ids=np.flatnonzero(hmask).astype(np.int32)+1
    ids_e=[]; val_e=[]; ids_s=[]; val_s=[]
    for r0 in range(0,2160,60):
        r1=min(2160,r0+60)
        rr=np.arange(r0,r1)
        latv=90-rr.astype(np.float64)*res
        # 2D rows x cols
        lm=landpix[r0:r1]
        if not lm.any(): continue
        rowidx,colidx=np.nonzero(lm)
        glat=latv[rowidx]; glon=lons[colidx]
        x,y=transformer.transform(glon,glat)
        hid=xy_to_id(np.asarray(x),np.asarray(y))
        valid=(hid>0)
        tmp=np.zeros_like(valid)
        tmp[valid]=hmask[hid[valid]-1]
        valid &= tmp
        if valid.any():
            ids_e.append(hid[valid]); val_e.append(z[r0:r1][rowidx[valid],colidx[valid]])
        # slope only for pixels with N/S/E/W all land
        sg=lm.copy()
        if r0==0: sg[0,:]=False
        if r1==2160: sg[-1,:]=False
        # Need neighbors from global mask, not chunk-local only.
        rg=rr[rowidx]; cg=colidx
        interior=(rg>0)&(rg<2159)&(cg>0)&(cg<4319)
        if interior.any():
            rg2=rg[interior]; cg2=cg[interior]
            nb=landpix[rg2-1,cg2]&landpix[rg2+1,cg2]&landpix[rg2,cg2-1]&landpix[rg2,cg2+1]
            if nb.any():
                rg3=rg2[nb]; cg3=cg2[nb]
                lat3=90-rg3.astype(np.float64)*res; lon3=lons[cg3]
                x3,y3=transformer.transform(lon3,lat3); id3=xy_to_id(np.asarray(x3),np.asarray(y3))
                vg=(id3>0); t=np.zeros_like(vg); t[vg]=hmask[id3[vg]-1]; vg &= t
                if vg.any():
                    rg4=rg3[vg]; cg4=cg3[vg]; id4=id3[vg]
                    dy=111132.0*res
                    dx=np.maximum(25.0,111320.0*np.cos(np.deg2rad(lat3[vg]))*res)
                    dzdx=(z[rg4,cg4+1]-z[rg4,cg4-1])/(2*dx)
                    dzdy=(z[rg4-1,cg4]-z[rg4+1,cg4])/(2*dy)
                    sl=np.degrees(np.arctan(np.sqrt(dzdx*dzdx+dzdy*dzdy))).astype(np.float32)
                    ids_s.append(id4); val_s.append(sl)
        print('ROWS',r0,r1,'elev_samples',sum(len(v) for v in ids_e),'slope_samples',sum(len(v) for v in ids_s),flush=True)
    ids_e=np.concatenate(ids_e); val_e=np.concatenate(val_e); ids_s=np.concatenate(ids_s); val_s=np.concatenate(val_s)
    print('ACCEPTED',len(ids_e),len(ids_s),flush=True)
    es=group_stats(ids_e,val_e,'ELEV',all_land_ids)
    ss=group_stats(ids_s,val_s,'SLOPE',all_land_ids)
    df=pd.DataFrame({'id':all_land_ids})
    for k,v in es.items(): df[k]=v
    # For slope keep N, mean, p90 and max; other quantiles still useful for audit.
    for k,v in ss.items(): df[k]=v
    df['RELIEF_P90P10']=df['ELEV_P90']-df['ELEV_P10']
    df['ELEV_RANGE']=df['ELEV_MAX']-df['ELEV_MIN']
    df['DEM_SRC']='ETOPO5_5arcmin_numeric'
    df['DEM_SOURCE_USED']=src
    df['ETOPO5_SHA256']=sha256(work/'ETOPO5.DAT')
    df['row_index']=(df.id-1)%ROWS; df['col_index']=(df.id-1)//ROWS
    cols=['id','row_index','col_index','ELEV_N','ELEV_MIN','ELEV_P10','ELEV_MEAN','ELEV_MED','ELEV_P90','ELEV_MAX','RELIEF_P90P10','ELEV_RANGE','SLOPE_N','SLOPE_MIN','SLOPE_P10','SLOPE_MEAN','SLOPE_MED','SLOPE_P90','SLOPE_MAX','DEM_SRC','DEM_SOURCE_USED','ETOPO5_SHA256']
    df[cols].to_csv(a.out,index=False)
    summ={'land_hexes':int(len(df)),'elev_zero_sample_hexes':int((df.ELEV_N==0).sum()),'slope_zero_sample_hexes':int((df.SLOPE_N==0).sum()),'elev_samples':int(len(ids_e)),'slope_samples':int(len(ids_s)),'source_used':src,'etopo5_sha256':sha256(work/'ETOPO5.DAT')}
    Path('CIV_GAME_MAP_STAGE1B_ETOPO5_5MIN_SUMMARY.json').write_text(json.dumps(summ,indent=2),encoding='utf-8')
    print(json.dumps(summ,indent=2),flush=True)

if __name__=='__main__': main()