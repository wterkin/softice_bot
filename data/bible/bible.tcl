#########################################
#                                       #
#     bible.tcl v1.1 Bible Script       #
#                                       #
#      author: leonidas@*.rusnet        #
#                                       #
#       url: http://sopov.ru/           #
#                                       #
#  support: irc://irc.rinnet.ru/#jesus  #
#                                       #
##########################################################################
#
#  script home page : http://sopov.ru/coding/bible.shtml
#
#  v1.1  [27 Nov 2005] - update bible base and search is added
#       !find <text>   - find text in bible
#       !findnt <text> - find text in new testament 
#       !findot <text> - find text in old testament
#
#  v1.05 [23 Mar 2005] - added flag nopubbible and fixed small bug's
#
#  v1.04 [ 7 Feb 2005] - added additional name for Isaiah
#
#  v1.03 [26 Jan 2005] - fixed Psalm book counts verses 
#
#  v1.02 [20 Jan 2005] - fixed Daniel counts verses
#    access command:
#       !bible <book> <chapter>:<verse>[-<verse>]  - quoting block verses
#
#  v1.01 [17 Jan 2005] - added in book "dot"-sign
#	   !bible Jn 1:1 == !bible Jn. 1:1
#
#  v1.0  [15 Jan 2005] - start script 
#    access command:
#       !books   - books list
#	!bible <book> <chapter>:<verse>  - read bible verses 
#
##########################################################################
bind pub	-	.bible		pub_bible
bind msg	-	.bible		msg_bible
bind pub	-	.books		pub_books
bind msg	-	.books		msg_books

bind pub	-	.библия		pub_bible
bind pub	-	.б		pub_bible
bind msg	-	.библия		msg_bible
bind pub	-	.стих		pub_bible
bind msg	-	.стих		msg_bible
bind pub	-	.книги		pub_books
bind msg	-	.книги		msg_books

bind pub	-	.find		pub_find
bind msg	-	.find		msg_find
bind pub	-	.findnt		pub_findnt
bind msg	-	.findnt		msg_findnt
bind pub	-	.findot		pub_findot
bind msg	-	.findot		msg_findot

bind pub	-	.найти		pub_find
bind msg	-	.найти		msg_find
bind pub	-	.найтинз	pub_findnt
bind msg	-	.найтинз	msg_findnt
bind pub	-	.найтивз	pub_findot
bind msg	-	.найтивз	msg_findot

#########################################

# source book directory
set bbdir		"rus"


# send usage via NOTICE/PRIVMSG?
## on !bible
set bbusage		"PRIVMSG"
## on !find
set bbusage_find	"PRIVMSG"
## on !books
set bbusage_book	"NOTICE"
## error
set bbusage_err		"NOTICE"

# send readings to nick/channel
set bbread		"channel"
set bbfind		"channel"

# max verses with citing (if fun command !bible Psalom 118:1-176 :-) )
set maxvers 10
# count finded
set findcnt 3

#########################################
#                                       #
#       further nothing change          #
#                                       #
#########################################

set bible_letter	""
set bible_ver		"1.1"
set bible_authors	"leonidas@*.rusnet http://sopov.ru/"

## for disable script
setudef flag nopubbible

#########################################
set bible_books "*1* Бытие Быт 50 31 25 24 26 32 22 24 22 29 32 32 20 18 24 21 16 27 33 38 18 34 24 20 67 34 35 46 22 35 43 55 32 20 31 29 43 36 30 23 23 57 38 34 34 28 34 31 22 33 26
*2* Исход Исх 40 22 25 22 31 23 30 25 32 35 29 10 51 22 31 27 36 16 27 25 26 36 31 33 18 40 37 21 43 46 38 18 35 23 35 35 38 29 31 43 38
*3* Левит Лев 27 17 16 17 35 19 30 38 36 24 20 47 8 59 57 33 34 16 30 37 27 24 33 44 23 55 46 34
*4* Числа Числ 36 54 34 51 49 31 27 89 26 23 36 35 16 33 45 41 50 13 32 22 29 35 41 30 25 18 65 23 31 40 16 54 42 56 29 34 13
*5* Второзаконие Втор 34 46 37 29 49 33 25 26 20 29 22 32 32 18 29 23 22 20 22 21 20 23 30 25 22 19 19 26 68 29 20 30 52 29 12
*6* ИНавин Нав 24 18 24 17 24 15 27 26 35 27 43 23 24 33 15 63 10 18 28 51 9 45 34 16 33
*7* Судей Суд 21 36 23 31 24 31 40 25 35 57 18 40 15 25 20 20 31 13 31 30 48 9 25
*8* Руфь Руфь 4 22 23 18 22
*9* 1Царств 1Цар 31 28 36 21 22 12 21 17 22 27 27 15 25 23 52 35 23 58 30 24 42 15 23 29 22 44 25 12 25 11 31 13
*10* 2Царств 2Цар 24 27 32 39 12 25 23 29 18 13 19 27 31 39 33 37 23 29 33 43 26 22 51 39 25
*11* 3Царств 3Цар 22 53 46 28 34 18 38 51 66 28 29 43 33 34 31 34 34 24 46 21 43 29 53
*12* 4Царств 4Цар 25 18 25 27 44 27 33 20 29 37 36 21 21 25 29 38 20 41 37 37 21 26 20 37 20 30
*13* 1Паралипоменон 1Пар 29 54 55 24 43 26 81 40 40 44 14 47 39 14 17 29 43 27 17 19 8 30 19 32 31 31 32 34 21 30
*14* 2Паралипоменон 2Пар 36 17 18 17 22 14 42 22 18 31 19 23 16 22 15 19 14 19 34 11 37 20 12 21 27 28 23 9 27 36 27 21 33 25 33 27 23
*15* Ездра Езд 10 11 70 13 24 17 22 28 36 15 44
*16* Неемия Неем 13 11 20 32 23 19 19 73 18 38 39 36 47 31
*17* Есфирь Есф 10 22 23 15 17 14 14 10 17 32 3
*18* Иов Иов 42 22 13 26 21 27 30 21 22 35 22 20 25 28 22 35 22 16 21 29 29 34 30 17 25 6 14 23 28 25 31 40 22 33 37 16 33 24 41 30 24 34 17
*19* Псалтирь Пс 150 6 12 9 9 13 11 18 10 39 7 9 6 7 5 11 15 51 18 10 14 32 6 10 22 12 14 9 11 13 25 11 22 23 28 13 40 23 14 18 14 12 5 27 18 12 10 15 21 23 21 11 7 9 24 14 12 12 18 14 9 13 12 11 14 20 8 36 37 6 24 20 28 23 11 13 21 72 13 20 17 8 19 13 14 17 7 19 53 17 16 16 5 23 11 13 12 9 9 5 8 29 22 35 45 48 43 14 31 7 10 10 9 26 9 10 2 29 176 7 8 9 4 8 5 6 5 6 8 8 3 18 3 3 21 26 9 8 24 14 10 7 12 15 21 10 11 9 14 9 6
*20* Причти Притч 31 23 22 35 27 23 35 27 36 18 32 31 28 25 35 33 33 28 24 29 30 31 29 35 34 28 28 27 28 27 33 31
*21* Екклесиаст Еккл 12 18 26 22 16 20 12 29 17 18 20 10 14
*22* Песни Песн 8 17 17 11 16 16 13 13 14
*23* Исаии Ис 66 31 22 26 6 30 13 25 22 21 34 16 6 22 32 9 14 14 7 25 6 17 25 18 23 12 21 13 29 24 33 9 20 24 17 7 22 38 22 8 31 29 25 28 28 25 13 15 22 26 11 23 15 12 17 13 12 21 14 21 22 11 12 19 12 25 24
*24* Иеремии Иер 52 19 37 25 31 31 30 34 22 26 25 23 17 27 22 21 21 27 23 15 18 14 30 40 10 38 24 22 17 32 24 40 44 26 22 19 32 21 28 18 16 18 22 13 30 5 28 7 47 39 46 64 34
*25* ПлачИеремии Плач 5 22 22 66 22 22
*26* Иезекииль Иез 48 28 10 27 17 17 14 27 18 11 22 25 28 23 23 8 63 24 32 14 49 32 31 49 27 17 21 36 26 21 26 18 32 33 31 15 38 28 23 29 49 26 20 27 31 25 24 23 35
*27* Даниил Дан 12 21 49 33 34 31 28 28 27 27 21 45 13
*28* Осия Ос 14 11 23 5 19 15 11 16 14 17 15 12 14 16 9
*29* Иоиль Иоиль 3 20 32 21
*30* Амос Ам 9 15 16 15 13 27 14 17 14 15
*31* Авдия Ав 1 21
*32* Иона Иона 4 17 10 10 11
*33* Михей Мих 7 16 13 12 13 15 16 20
*34* Наум Наум 3 15 13 19
*35* Аввакум Авв 3 17 20 19
*36* Софония Соф 3 18 15 20
*37* Аггей Агг 2 15 23
*38* Захария Зах 14 21 13 10 14 11 15 14 23 17 12 17 14 9 21
*39* Малахия Мал 4 14 17 18 6
*40* Матфей Мф 28 25 23 17 25 48 34 29 34 38 42 30 50 58 36 39 28 27 35 30 34 46 46 39 51 46 75 66 20
*41* Марка Мк 16 45 28 35 41 43 56 37 38 50 52 33 44 37 72 47 20
*42* Луки Лк 24 80 52 38 44 39 49 50 56 62 42 54 59 35 35 32 31 37 43 48 47 38 71 56 53
*43* Иоанна ин 21 51 25 36 54 47 71 53 59 41 42 57 50 38 31 27 33 26 40 42 31 25
*44* Деяния Деян 28 26 47 26 37 42 15 60 40 43 48 30 25 52 28 41 40 34 28 41 38 40 30 35 27 27 32 44 31
*45* Иакова Иак 5 27 26 18 17 20
*46* 1Петра 1Пет 5 25 25 22 19 14
*47* 2Петра 2Пет 3 21 22 18
*48* 1Иоанна 1Ин 5 10 29 24 21 21
*49* 2Иоанна 2Ин 1 13
*50* 3Иоанна 3Ин 1 14
*51* Иуды Иуд 1 25
*52* Римлянам Рим 16 32 29 31 25 21 23 25 39 33 21 36 21 14 23 33 27
*53* 1Коринфянам 1Кор 16 31 16 23 21 13 20 40 13 27 33 34 31 13 40 58 24
*54* 2Коринфянам 2Кор 13 24 17 18 18 21 18 16 24 15 18 33 21 14
*55* Галатам Гал 6 24 21 29 31 26 18
*56* Ефесянам Еф 6 23 22 21 32 33 24
*57* Филиппийцам Флп 4 30 30 21 23
*58* Колоссянам Кол 4 29 23 25 18
*59* 1Фессалоникийцам 1Фес 5 10 20 13 18 28
*60* 2Фессалоникийцам 2Фес 3 12 17 18
*61* 1Тимофею 1Тим 6 20 15 16 16 25 21
*62* 2Тимофею 2Тим 4 18 26 17 22
*63* Титу Тит 3 16 15 15
*64* Филимону Флм 1 25
*65* Евреям Евр 13 14 18 19 16 14 20 28 13 28 39 40 29 25
*66* Откровение Откр 22 20 29 22 11 14 17 17 13 21 11 19 17 18 20 8 21 18 24 21 15 27 21"

################################
proc bible_check {tip book chapter verse verse02 whom nick uhost} {
	global bible_books bbusage_err bbdir maxvers
set poss 0
if {[regexp  -nocase {^(Быт|Бт|Бытие|Ge|Gen|Gn|Genesis)(\.)?$} $book]} {set poss 1}
if {[regexp  -nocase {^(Исх|Исход|Ex|Exo|Exod|Exodus)(\.)?$} $book]} {set poss 2}
if {[regexp  -nocase {^(Лев|Лв|Левит|Lev|Le|Lv|Levit|Leviticus)(\.)?$} $book]} {set poss 3}
if {[regexp  -nocase {^(Чис|Чс|Числ|Числа|Nu|Num|Nm|Numb|Numbers)(\.)?$} $book]} {set poss 4}
if {[regexp  -nocase {^(Втор|Вт|Втрзк|Втрзк|Второзаконие|De|Deut|Deu|Dt)(\.)?$} $book]} {set poss 5}
if {[regexp  -nocase {^(ИисНав|Нав|ИисусНавин|Jos|Josh|Joshua)(\.)?$} $book]} {set poss 6}
if {[regexp  -nocase {^(Суд|Сд|Судьи|Jdg|Judg|Judge|Judges)(\.)?$} $book]} {set poss 7}
if {[regexp  -nocase {^(Руф|Рф|Руфь|Ru|Ruth|Rth|Rt)(\.)?$} $book]} {set poss 8}
if {[regexp  -nocase {^1?(Цар|Цр|Ц|Царств|Sa|S|Sam|Sm|Sml|Samuel)(\.)?$} $book]} {set poss 9}
if {[regexp  -nocase {^2(Цар|Цр|Ц|Царств|Sa|S|Sam|Sm|Sml|Samuel)(\.)?$} $book]} {set poss 10}
if {[regexp  -nocase {^3(Цар|Цр|Ц|Царств|Sa|S|Sam|Sm|Sml|Samuel)(\.)?$} $book]} {set poss 11}
if {[regexp  -nocase {^1?(Ki|K|Kn|Kg|King)(\.)?$} $book]} {set poss 11}
if {[regexp  -nocase {^4(Цар|Цр|Ц|Царств|Sa|S|Sam|Sm|Sml|Samuel)(\.)?$} $book]} {set poss 12}
if {[regexp  -nocase {^2(Ki|K|Kn|Kg|King)(\.)?$} $book]} {set poss 12}
if {[regexp  -nocase {^1?(Пар|Паралипоменон|Chr|Ch|Chron)(\.)?$} $book]} {set poss 13}
if {[regexp  -nocase {^2(Пар|Паралипоменон|Chr|Ch|Chron)(\.)?$} $book]} {set poss 14}
if {[regexp  -nocase {^(Ездр|Езд|Ез|Ездра|Ezr|Ezra)(\.)?$} $book]} {set poss 15}
if {[regexp  -nocase {^(Неем|Нм|Неемия|Ne|Neh|Nehem|Nehemiah)(\.)?$} $book]} {set poss 16}
if {[regexp  -nocase {^(Есф|Ес|Есфирь|Esth|Est|Esther)(\.)?$} $book]} {set poss 17}
if {[regexp  -nocase {^(Иов|Ив|Job|Jb)(\.)?$} $book]} {set poss 18}
if {[regexp  -nocase {^(Пс|Псалт|Псал|Псл|Псалом|Псалтирь|Псалмы|Ps|Psa|Psal|Psalms)(\.)?$} $book]} {set poss 19}
if {[regexp  -nocase {^(Прит|Притч|Пр|Притчи|Притча|Pr|Prov|Pro|Proverbs)(\.)?$} $book]} {set poss 20}
if {[regexp  -nocase {^(Еккл|Ек|Екк|Екклесиаст|Ec|Eccl|Ecc|Ecclesia|Ecclesia)(\.)?$} $book]} {set poss 21}
if {[regexp  -nocase {^(Песн|Пес|Псн|Песн(и|я)?Песней|Песни|Song|SongSongs|SS|Sol)(\.)?$} $book]} {set poss 22}
if {[regexp  -nocase {^(Ис|Иса|Иса[ий][ия]|Isa|Is|Isaiah)(\.)?$} $book]} {set poss 23}
if {[regexp  -nocase {^(Иер|Иерем|Иеремия|Je|Jer|Jerem|Jeremiah)(\.)?$} $book]} {set poss 24}
if {[regexp  -nocase {^(Плач|Плч|Пл|ПлИер|ПлачИеремии|La|Lam|Lament)(\.)?$} $book]} {set poss 25}
if {[regexp  -nocase {^(Иез|Из|Иезек|Иезекииль|Ez|Eze|Ezek|Ezekiel)(\.)?$} $book]} {set poss 26}
if {[regexp  -nocase {^(Дан|Дн|Днл|Даниил|Da|Dan|Daniel)(\.)?$} $book]} {set poss 27}
if {[regexp  -nocase {^(Ос|Осия|Hos|Ho|Hosea)(\.)?$} $book]} {set poss 28}
if {[regexp  -nocase {^(Иоил|Ил|Иоиль|Joel|Joe)(\.)?$} $book]} {set poss 29}
if {[regexp  -nocase {^(Ам|Амс|Амос|Am|Amos|Amo)(\.)?$} $book]} {set poss 30}
if {[regexp  -nocase {^(Авд|Авдий|Ob|Obad|Obadiah|Oba)(\.)?$} $book]} {set poss 31}
if {[regexp  -nocase {^(Ион|Иона|Jon|Jnh|Jona|Jonah)(\.)?$} $book]} {set poss 32}
if {[regexp  -nocase {^(Мих|Мх|Михей|Mi|Mic|Micah)(\.)?$} $book]} {set poss 33}
if {[regexp  -nocase {^(Наум|Na|Nah|Nahum)(\.)?$} $book]} {set poss 34}
if {[regexp  -nocase {^(Авв|Аввак|Аввакум|Hab|Habak|Habakkuk)(\.)?$} $book]} {set poss 35}
if {[regexp  -nocase {^(Соф|Софон|Софония|Zeph|Zep|Zephaniah)(\.)?$} $book]} {set poss 36}
if {[regexp  -nocase {^(Агг|Аггей|Hag|Haggai)(\.)?$} $book]} {set poss 37}
if {[regexp  -nocase {^(Зах|Зхр|Захар|Захария|Ze|Zec|Zech|Zechariah)(\.)?$} $book]} {set poss 38}
if {[regexp  -nocase {^(Мал|Малах|Млх|Малахия|Mal|Malachi)(\.)?$} $book]} {set poss 39}
if {[regexp  -nocase {^(Матф|Мтф|Мф|Мт|Матфея|Матфей|Мат|Mt|Ma|Matt|Mat|Matthew)(\.)?$} $book]} {set poss 40}
if {[regexp  -nocase {^(Мар|Марк|Мрк|Мр|Марка|Мк|Mk|Mk|Mar|Mr|Mrk|Mark)(\.)?$} $book]} {set poss 41}
if {[regexp  -nocase {^(Лук|Лк|Лукa|Луки|Lk|Lu|Luk|Luke)(\.)?$} $book]} {set poss 42}
if {[regexp  -nocase {^(Иоан|Ин|Иоанн|Иоанна|Jn|Jno|Jo|Joh|John)(\.)?$} $book]} {set poss 43}
if {[regexp  -nocase {^(Деян|Дея|ДА|Деяния|Ac|Act|Acts)(\.)?$} $book]} {set poss 44}
if {[regexp  -nocase {^(Иак|Ик|Иаков|Иакова|Jas|Ja|Jam|Jms|James)(\.)?$} $book]} {set poss 45}
if {[regexp  -nocase {^1?(Пет|Пт|Птр|Петр|Петра|Pe|Pet|Peter)(\.)?$} $book]} {set poss 46}
if {[regexp  -nocase {^2(Пет|Пт|Птр|Петр|Петра|Pe|Pet|Peter)(\.)?$} $book]} {set poss 47}
if {[regexp  -nocase {^1(Иоан|Ин|Иоанн|Иоанна|Jn|Jno|Jo|Joh|John)(\.)?$} $book]} {set poss 48}
if {[regexp  -nocase {^2(Иоан|Ин|Иоанн|Иоанна|Jn|Jno|Jo|Joh|John)(\.)?$} $book]} {set poss 49}
if {[regexp  -nocase {^3(Иоан|Ин|Иоанн|Иоанна|Jn|Jno|Jo|Joh|John)(\.)?$} $book]} {set poss 50}
if {[regexp  -nocase {^(Иуд|Ид|Иуда|Иуды|Jud|Jude|Jd|Jd)(\.)?$} $book]} {set poss 51}
if {[regexp  -nocase {^(Рим|Римл|Римлянам|Ro|Rom|Romans)(\.)?$} $book]} {set poss 52}
if {[regexp  -nocase {^1?(Кор|Коринф|Коринфянам|Co|Cor|Corinth|Corinthians)(\.)?$} $book]} {set poss 53}
if {[regexp  -nocase {^2(Кор|Коринф|Коринфянам|Co|Cor|Corinth|Corinthians)(\.)?$} $book]} {set poss 54}
if {[regexp  -nocase {^(Гал|Галат|Галатам|Ga|Gal|Galat|Galatians)(\.)?$} $book]} {set poss 55}
if {[regexp  -nocase {^(Еф|Ефес|Ефесянам|Eph|Ep|Ephes|Ephes|Ephesians)(\.)?$} $book]} {set poss 56}
if {[regexp  -nocase {^(Фил|Флп|Филип|Филиппийцам|Филипийцам|Php|Ph|Phil|Phi)(\.)?$} $book]} {set poss 57}
if {[regexp  -nocase {^(Кол|Колос|Колоссянам|Col|Colos|Colossians)(\.)?$} $book]} {set poss 58}
if {[regexp  -nocase {^1?(Фесс|Фес|Фессалоникийцам|Сол|Солунянам|Th|Thes|Thess|Thessalonians)(\.)?$} $book]} {set poss 59}
if {[regexp  -nocase {^2(Фесс|Фес|Фессалоникийцам|Сол|Солунянам|Th|Thes|Thess|Thessalonians)(\.)?$} $book]} {set poss 60}
if {[regexp  -nocase {^1?(Тим|Тимоф|Тимофею|Ti|Tim|Timothy)(\.)?$} $book]} {set poss 61}
if {[regexp  -nocase {^2(Тим|Тимоф|Тимофею|Ti|Tim|Timothy)(\.)?$} $book]} {set poss 62}
if {[regexp  -nocase {^(Тит|Титу|Tit|Ti|Titus)(\.)?$} $book]} {set poss 63}
if {[regexp  -nocase {^(Флм|Филимон|Филимону|Phm|Phile|Phile|Phlm|Phlm|Philemon)(\.)?$} $book]} {set poss 64}
if {[regexp  -nocase {^(Евр|Евреям|He|Heb|Hebr|Hebrews)(\.)?$} $book]} {set poss 65}
if {[regexp  -nocase {^(Откр|Отк|Откровен|Апок|Откровение|Апокалипсис|Rev|Re|Rv|Revelation)(\.)?$} $book]} {set poss 66}
if {![regexp {^([1-9]|[1-5][0-9]|6[0-6])$} $poss]} {
		putserv "$bbusage_err $nick :\00302мне не известна такая книга"
		return 0
	}
	if {$verse > $verse02} {
	  	putserv "$bbusage_err $nick :начальный стих должен быть меньше конечного"
	  	return 0;
	}
	if {$maxvers <= $verse02-$verse} {
	  	putserv "$bbusage_err $nick :можно за раз процитировать только \00302$maxvers\003 ст."
	  	return 0;
	}
	if { [regexp -line [subst {(\\*$poss\\*)(.*)}] $bible_books math buf buf1] == "1" } {
	  set bookn [lindex $buf1 0]
	  set maxc [lindex $buf1 2]
	  if {$maxc < $chapter} {
	  	putserv "$bbusage_err $nick :в книге \00302$bookn\003: \00302$maxc\003 гл."
	  	return 0;
	  } 
	  set maxv [lindex $buf1 [expr 2 + $chapter]]
	  if {$maxv < $verse02} {
	  	putserv "$bbusage_err $nick :в книге \00302$bookn\003 в \00302$chapter\003 главе: \00302$maxv\003 ст."
	  	return 0;
	  }
	  set fd [open $bbdir/$poss.dat r]
	  set chop [read $fd]
	  close $fd
	  	if {$verse == $verse02} {
	  		regexp -line [subst {^($chapter:$verse:)(.*)}] $chop m1 m2 m3
	  
			putserv "$tip $whom :\00304$bookn $chapter:$verse"
	  		putserv "$tip $whom :\00302$m3"
		} else {
			putserv "$tip $whom :\00304$bookn $chapter:$verse-$verse02"
			for {set x $verse} {$x <= $verse02} {incr x} {
			regexp -line [subst {^($chapter:$x:)(.*)}] $chop m1 m2 m3
		        putserv "$tip $whom :\00314$x. \00302$m3"
			}
		}
	}
}

proc bible {uhost tip whom nick arg} {
	global bbusage_err bible_books
		set book [lindex $arg 0]
		set buf [lindex $arg 1]
		set verse02 0
		set error_trap [regexp {([1-9][0-9]*)[:\.]([1-9][0-9]*)(-([1-9][0-9]*))?} $buf match chapter verse verse2 verse02]
		if {$error_trap == "0"} {
			set chapter ""
			set verse ""
			set verse2 ""
			set verse02 0
		}
	#set krom [$bible_books buf buf1]
	#putserv "$tip $whom :необходимо процитировать книгу $book  главу $chapter стих $verse // $krom"

		if {$book == "" || $chapter == "" || $verse == ""} {
			putserv "$bbusage_err $nick :\00302стоит вводить в формате:"
			putserv "$bbusage_err $nick :\00304!библия <книга> <глава>:<стих>\[-<стих>\]"
			return 0
		}
		if {![regexp {^[0-9]+$} $verse02]} {
			set verse02 0
		}
		if {![regexp {^[1-9][0-9]*$} $verse] || ![regexp {^[0-9]+$} $verse02] || ![regexp {^[1-9][0-9]*$} $chapter]} {
			putserv "$bbusage_err $nick :\00302что то пишем мы не такс..."
	
		return 0
		}
		if {![regexp {^[1-9][0-9]*$} $verse02]} {
			bible_check $tip $book $chapter $verse $verse $whom $nick $uhost
		 } else {
			bible_check $tip $book $chapter $verse $verse02 $whom $nick $uhost
		}
}
proc books {nick uhost arg} {
	global bbusage_book
	set wht [lindex $arg 0]
		if {$wht == "ot" || $wht == "вз"} {
			putserv "$bbusage_book $nick :\00304Книги Моисея: \00302Бытие, Исход, Левит, Числа, Второзаконие"
			putserv "$bbusage_book $nick :\00304Историческии: \00302ИНавин, Судей, Руфь, 1Царств, 2Царств, 3Царств, 4Царств, 1Паралипоменон, 2Паралипоменон, Ездра, Иеемия, Есфирь"
			putserv "$bbusage_book $nick :\00304Учительные: \00302Иов, Псалтрирь, Причти, Екклесиаст, Песни"
			putserv "$bbusage_book $nick :\00304Пророчиеские: \00302Исаии, Иеремии, ПлачИеремии, Иезекииль, Даниил, Осия, Иоиль, Амос, Авдий, Иона, Михей, Наум, Аввакум, Софония, Аггей, Захария, Малахия"
		}
		if {$wht == "nt" || $wht == "нз"} {
			putserv "$bbusage_book $nick :\00304Жизнь Иисуса Христа и Первой Церкви: \00302Матфей, Марка, Луки, Иоанна, Деяния"
			putserv "$bbusage_book $nick :\00304Послания Апостола Павла к Церквям: \00302Римлянам, 1Коринфянам, 1Коринфянам,Галатам, Ефесянам, Филиппийцам, Колоссянам, 1Фессалоникийцам, 2Фессалоникийцам"
			putserv "$bbusage_book $nick :\00304Личные Послания Апостола Павла: \003021Тимофею, 2Тимофею, Титу, Филимону"
			putserv "$bbusage_book $nick :\00304Главные послания Апостолов и Пророков: \00302Евреям, Иакова, 1Петра, 2Петра, 1Иоанна, 2Иоанна, 3Иоанна, Иуды"
			putserv "$bbusage_book $nick :\00304Пророчества: \00302Откровение"
		}
		if {$wht == ""} {
			putserv "$bbusage_book $nick :\00304Книги Моисея: \00302Бытие, Исход, Левит, Числа, Второзаконие"
			putserv "$bbusage_book $nick :\00304Историческии: \00302ИНавин, Судей, Руфь, 1Царств, 2Царств, 3Царств, 4Царств, 1Паралипоменон, 2Паралипоменон, Ездра, Иеемия, Есфирь"
			putserv "$bbusage_book $nick :\00304Учительные: \00302Иов, Псалтрирь, Причти, Екклесиаст, Песни"
			putserv "$bbusage_book $nick :\00304Пророчиеские: \00302Исаии, Иеремии, ПлачИеремии, Иезекииль, Даниил, Осия, Иоиль, Амос, Авдий, Иона, Михей, Наум, Аввакум, Софония, Аггей, Захария, Малахия"
			putserv "$bbusage_book $nick :\00304Жизнь Иисуса Христа и Первой Церкви: \00302Матфей, Марка, Луки, Иоанна, Деяния"
			putserv "$bbusage_book $nick :\00304Послания Апостола Павла к Церквям: \00302Римлянам, 1Коринфянам, 1Коринфянам,Галатам, Ефесянам, Филиппийцам, Колоссянам, 1Фессалоникийцам, 2Фессалоникийцам"
			putserv "$bbusage_book $nick :\00304Личные Послания Апостола Павла: \003021Тимофею, 2Тимофею, Титу, Филимону"
			putserv "$bbusage_book $nick :\00304Главные послания Апостолов и Пророков: \00302Евреям, Иакова, 1Петра, 2Петра, 1Иоанна, 2Иоанна, 3Иоанна, Иуды"
			putserv "$bbusage_book $nick :\00304Пророчества: \00302Откровение"
		}		
}

################################
proc pub_books {nick uhost hand chan arg} {
if {[channel get $chan nopubbible]} return
	books $nick $uhost $arg
}
proc msg_books {nick uhost hand arg} {
	global bbusage bbread
	books $nick $uhost $arg
}

proc pub_bible {nick uhost hand chan arg} {
if {[channel get $chan nopubbible]} return
	global bbusage bbread
	if {$bbread == "nick"} {
		bible $uhost $bbusage $nick $nick $arg
	} else {
		bible $uhost $bbusage $chan $nick $arg
	}
}
proc msg_bible {nick uhost hand arg} {
	global bbusage
		bible $uhost $bbusage $nick $nick $arg
	
}
#########################################

proc findb {uhost tip whom nick nt ot arg} {
		global bbusage_err bible_books cntfnd bbdir findcnt
		set fnd [tolower $arg]
		if {$nt == "on"} {
			if {$ot == "on"} {
			set start 1
			set bn "ветхого и нового завета"
			} else {
			set start 40
			set bn "нового завета"
			}
			set end 67
		} else {
			if {$ot == "on"} {
			set end 40
			set bn "ветхого завета"
			} else {
			set end 0
			}
			set start 1
		}

		set lenfnd [string bytelength $fnd]
		if { [expr ($lenfnd / 2)] < 4} {
		putserv "$bbusage_err $nick :слишком короткий текст для поиска"
		return 0
		}
		if { [expr ($lenfnd / 2)] > 40 } {
		putserv "$bbusage_err $nick :слишком длинный текст для поиска [$lenfnd]"
		return 0
		}
		if { $lenfnd == 0} {
		putserv "$bbusage_err $nick :Книги для поиска не заданны"
		return 0
		}

 
		putserv "$tip $whom :\00302ищем\00304 $fnd \00302в книгах\00304 $bn"
		set allfind 0;
		for {set x $start} {$x < $end} {incr x} {
		if { $allfind >= 5 } {
			break
			}
		set curfind 0; 
		set fp [open "$bbdir/$x.dat" r]
		while {![eof $fp]} {
			if { $allfind >= $findcnt } {
			break
			}
			set line [gets $fp]
		        set lines [tolower $line]
			
			set findok [string first $fnd $lines]
			if {$findok != -1} {
				if { [regexp -line [subst {(\\*$x\\*)(.*)}] $bible_books math buf buf1] == "1" } {
					set bookn [lindex $buf1 0]		
					regexp {([0-9]+:[0-9]+):(.*)} $line - where findline
					putserv "$tip $whom :\00304$bookn $where \00302$findline"
				}
				incr allfind
				incr curfind;
			}

			

			if { $curfind > 1} {
				break
				}			
			

		}		
		close $fp
		

		}
		if {$allfind == 0} {putserv "$tip $whom :ничего не нашел"}
		set finfok 0
}
proc tolower {text} { return [string map {А а Б б В в Г г Д д Е е Ё ё Ж ж З з И и Й й К к Л л М м Н н О о П п Р р С с Т т У у Ф ф Х х Ц ц Ч ч Ш ш Щ щ Ъ ъ Ы ы Ь ь Э э Ю ю Я я} [string tolower $text]] }

########################################
proc pub_find {nick uhost hand chan arg} {
if {[channel get $chan nopubbible]} return
	global bbusage_find bbfind
	set nt "on"
	set ot "on"

	if {$bbfind == "nick"} {
		findb $uhost $bbusage_find $nick $nick $nt $ot $arg
	} else {
		findb $uhost $bbusage_find $chan $nick $nt $ot $arg
	}
}

proc msg_find {nick uhost hand arg} {
	global bbusage_find bbfind
	set nt "on"
	set ot "on"
	findb $uhost $bbusage_find $nick $nick $nt $ot $arg
	
}

proc pub_findnt {nick uhost hand chan arg} {
if {[channel get $chan nopubbible]} return
	global bbusage_find bbfind
	set nt "on"
	set ot "off"

	if {$bbfind == "nick"} {
		findb $uhost $bbusage_find $nick $nick $nt $ot $arg
	} else {
		findb $uhost $bbusage_find $chan $nick $nt $ot $arg
	}
}

proc msg_findnt {nick uhost hand arg} {
	global bbusage_find bbfind
	set nt "on"
	set ot "off"
	findb $uhost $bbusage_find $nick $nick $nt $ot $arg
	
}

proc pub_findot {nick uhost hand chan arg} {
if {[channel get $chan nopubbible]} return
	global bbusage_find bbfind
	set nt "off"
	set ot "on"

	if {$bbfind == "nick"} {
		findb $uhost $bbusage_find $nick $nick $nt $ot $arg
	} else {
		findb $uhost $bbusage_find $chan $nick $nt $ot $arg
	}
}

proc msg_findot {nick uhost hand arg} {
	global bbusage_find bbfind
	set nt "off"
	set ot "on"
	findb $uhost $bbusage_find $nick $nick $nt $ot $arg
}
########################################

putlog "bible.tcl v$bible_ver by $bible_authors loaded"
