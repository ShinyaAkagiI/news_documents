from pathlib import Path
from calculate_readability import calculate_readability
import re
import matplotlib.pyplot as plt

easy = Path("easy")
origin = Path("origin")

files = easy.glob("*")
fnames = [f.name for f in files]

# easyとoriginの比較
count = 0
valid_count = 0
easy_chars = 0
origin_chars = 0
easy_jfres = 0
origin_jfres = 0
for fname in fnames:
	easy_fname = easy / fname
	with open(easy_fname, "r") as f:
		data = f.read()
		easy_jfre = calculate_readability(data)["jfre"]

		# jFRE平均計算用
		easy_jfres += easy_jfre

		# 文字数平均計算用
		data = re.sub("[ 　\n]", "", data)
		easy_chars += len(data)

	origin_fname = origin / fname
	with open(origin_fname, "r") as f:
		data = f.read()
		origin_jfre = calculate_readability(data)["jfre"]

		# jFRE平均計算用
		origin_jfres += origin_jfre

		# 文字数平均計算用
		data = re.sub("[ 　\n]", "", data)
		origin_chars += len(data)

	# easyの方が読みやすいと判定された場合、valid_countを+1
	if easy_jfre > origin_jfre:
		valid_count += 1
	
	# 比較グラフ用
	plt.scatter(easy_jfre, origin_jfre, c="none", edgecolor="black")

	count += 1

print("NEWS WEB EASYの文字数平均：", easy_chars/len(fnames))
print("NEWS WEBの文字数平均：", origin_chars/len(fnames))
print("NEWS WEB EASYのjFRE平均：", easy_jfres/len(fnames))
print("NEWS WEBのjFRE平均：", origin_jfres/len(fnames))
print("NEWS WEB EASYの方を読みやすいとした文書数：{}/{}".format(valid_count, count))

plt.axline((20,20), (100,100), c="blue")
plt.xlim(0, 120)
plt.ylim(0, 120)
plt.xlabel("jFRE of NEWS WEB EASY", fontsize=14)
plt.ylabel("jFRE of NEWS WEB", fontsize=14)
plt.show()
