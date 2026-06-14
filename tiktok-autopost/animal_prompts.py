import random

THEMES = [
    {
        "prompt": "adorable baby red panda sitting on a bamboo branch, looking directly at camera with curious expression, soft forest background, golden hour lighting, photorealistic, 8k",
        "negative": "ugly, deformed, low quality, blurry, human",
        "caption": "レッサーパンダがこっちを見てる👀",
        "hashtags": "#レッサーパンダ #癒し #動物 #귀여워 #kawaii #animals #cute #foryou",
        "title": "レッサーパンダの視線がたまらない🐾",
    },
    {
        "prompt": "fluffy golden retriever puppy discovering snow for the first time, playful expression, snowy park, soft natural lighting, photorealistic, adorable, heartwarming",
        "negative": "ugly, deformed, low quality",
        "caption": "初雪に大興奮な子犬🐶❄️",
        "hashtags": "#ゴールデンレトリバー #子犬 #雪 #癒し #puppy #snow #dogs #foryou",
        "title": "初めての雪に子犬が大はしゃぎ❄️",
    },
    {
        "prompt": "tiny hedgehog eating a strawberry, extremely close up, studio lighting, white background, adorable expression, photorealistic",
        "negative": "ugly, deformed, low quality, blurry",
        "caption": "ちっちゃい口でイチゴを食べるハリネズミ🍓",
        "hashtags": "#ハリネズミ #癒し動画 #もふもふ #hedgehog #cute #animals #foryoupage",
        "title": "ハリネズミのイチゴタイム🍓",
    },
    {
        "prompt": "baby elephant learning to use its trunk, playful, sunny African savanna, mother elephant in background, photorealistic, warm tones, joyful atmosphere",
        "negative": "ugly, deformed, low quality",
        "caption": "鼻の使い方を練習中の赤ちゃんゾウ🐘",
        "hashtags": "#ゾウ #赤ちゃん動物 #アフリカ #elephant #baby #wildlife #nature #foryou",
        "title": "赤ちゃんゾウが鼻の練習中😂",
    },
    {
        "prompt": "curious cat discovering a butterfly that landed on its nose, wide eyes, garden background, soft bokeh, photorealistic, comic expression",
        "negative": "ugly, deformed, low quality",
        "caption": "鼻にチョウチョが止まってる！？🦋😳",
        "hashtags": "#猫 #ねこ #癒し #チョウチョ #cat #butterfly #neko #foryoupage",
        "title": "猫の鼻にチョウチョが！リアクション見て🦋",
    },
    {
        "prompt": "baby otter floating on its back in calm blue water, holding a small pebble, sunlight reflection on water, photorealistic, adorable, peaceful",
        "negative": "ugly, deformed, low quality",
        "caption": "川に浮かびながら石を持つカワウソ🦦",
        "hashtags": "#カワウソ #水辺の動物 #癒し #otter #cute #animals #nature #viral",
        "title": "カワウソが石を手放さない理由🦦💎",
    },
    {
        "prompt": "fluffy white bunny twitching its nose while nibbling on a carrot, extreme close up, soft pastel background, photorealistic, adorable",
        "negative": "ugly, deformed, low quality",
        "caption": "人参を食べながら鼻をひくひくさせるウサギ🐰🥕",
        "hashtags": "#うさぎ #ウサギ #癒し #rabbit #bunny #cute #foryou #animals",
        "title": "ウサギの鼻ひくひくが止まらない🐰",
    },
    {
        "prompt": "baby capybara relaxing in warm onsen hot spring water, steam rising, peaceful expression, Japanese bamboo garden background, photorealistic, serene",
        "negative": "ugly, deformed, low quality",
        "caption": "温泉でリラックスするカピバラ🛁♨️",
        "hashtags": "#カピバラ #温泉 #癒し #capybara #onsen #japan #animals #foryoupage",
        "title": "カピバラが温泉でリラックスしすぎてる😌",
    },
    {
        "prompt": "playful baby fox running through autumn leaves in a forest, russet and gold colors, photorealistic, joyful, dynamic movement",
        "negative": "ugly, deformed, low quality",
        "caption": "落ち葉の中を駆け回るキツネの子🦊🍂",
        "hashtags": "#キツネ #秋 #動物 #fox #autumn #cute #wildlife #foryou",
        "title": "秋の森を走り回る赤ちゃんキツネが可愛すぎ🦊",
    },
    {
        "prompt": "baby monkey hugging stuffed animal toy tightly while sleeping, soft jungle background, warm lighting, photorealistic, heartwarming, endearing",
        "negative": "ugly, deformed, low quality",
        "caption": "ぬいぐるみを抱いて眠る赤ちゃんサル🐒💤",
        "hashtags": "#サル #赤ちゃん動物 #癒し #monkey #baby #cute #animals #viral",
        "title": "ぬいぐるみを離さない赤ちゃんサル🐒",
    },
    {
        "prompt": "majestic white arctic fox sitting in fresh snow, piercing blue eyes looking at camera, snowflakes falling, photorealistic, ethereal beauty",
        "negative": "ugly, deformed, low quality",
        "caption": "雪の中のアークティックフォックス、美しすぎる🦊❄️",
        "hashtags": "#アークティックフォックス #北極 #動物 #arcticfox #snow #beautiful #wildlife #foryou",
        "title": "北極のキツネが美しすぎて見入る❄️",
    },
    {
        "prompt": "playful sea otter wrapping itself in kelp to sleep, floating peacefully on ocean surface, golden sunset, photorealistic, serene, wildlife photography",
        "negative": "ugly, deformed, low quality",
        "caption": "昆布で自分を包んで眠るラッコ🦦🌊",
        "hashtags": "#ラッコ #海 #癒し #seaotter #ocean #sleeping #animals #foryoupage",
        "title": "ラッコが昆布布団で就寝中😴🌿",
    },
    {
        "prompt": "chubby hamster stuffing its cheeks with sunflower seeds, extreme close up, soft pastel background, photorealistic, humorous expression, adorable",
        "negative": "ugly, deformed, low quality",
        "caption": "頬袋いっぱいに詰め込むハムスター🐹",
        "hashtags": "#ハムスター #頬袋 #癒し #hamster #cute #funny #animals #viral",
        "title": "ハムスターの頬袋パンパン事件🐹",
    },
    {
        "prompt": "baby koala clinging to mother's back, eucalyptus tree, soft morning light, photorealistic, sweet bonding moment, Australian wildlife",
        "negative": "ugly, deformed, low quality",
        "caption": "お母さんにしがみつく赤ちゃんコアラ🐨",
        "hashtags": "#コアラ #赤ちゃん動物 #癒し #koala #baby #australia #wildlife #foryou",
        "title": "赤ちゃんコアラがお母さんを離さない🐨💕",
    },
    {
        "prompt": "curious meerkat standing on hind legs, looking alert, Kalahari desert background, dramatic sunset sky, photorealistic, funny upright pose",
        "negative": "ugly, deformed, low quality",
        "caption": "ずっと見張り続けるミーアキャット👀",
        "hashtags": "#ミーアキャット #砂漠 #動物 #meerkat #desert #funny #wildlife #foryou",
        "title": "ミーアキャットの監視が本気すぎる😂",
    },
    {
        "prompt": "baby penguin chick peeking out from under parent's feathers, Antarctic landscape, black and white contrast, photorealistic, heartwarming, curious eyes",
        "negative": "ugly, deformed, low quality",
        "caption": "親ペンギンの羽の中からこんにちは🐧",
        "hashtags": "#ペンギン #赤ちゃん #南極 #penguin #baby #cute #wildlife #viral",
        "title": "ペンギンの赤ちゃんがひょっこり登場🐧",
    },
    {
        "prompt": "sleepy cat stretching dramatically after waking up, yawning with eyes squeezed shut, cozy indoor setting, warm afternoon light, photorealistic",
        "negative": "ugly, deformed, low quality",
        "caption": "全力でストレッチするネコの朝😸",
        "hashtags": "#猫 #ねこ #ストレッチ #朝 #cat #stretch #morning #neko #foryoupage",
        "title": "このネコのストレッチが全力すぎる🐱",
    },
    {
        "prompt": "baby sloth hanging upside down from branch, ultra slow movement, tropical rainforest, dappled sunlight through leaves, photorealistic, peaceful, endearing",
        "negative": "ugly, deformed, low quality",
        "caption": "ゆーっくり動くナマケモノの赤ちゃん🦥",
        "hashtags": "#ナマケモノ #熱帯雨林 #癒し #sloth #baby #jungle #cute #foryou",
        "title": "ナマケモノのスロー生活が羨ましい🦥",
    },
    {
        "prompt": "duckling following its mother in a line through a garden pond, morning mist, soft pastel colors, photorealistic, peaceful countryside atmosphere",
        "negative": "ugly, deformed, low quality",
        "caption": "お母さんガモのあとをついて行く子鴨ちゃん🐥",
        "hashtags": "#アヒル #子鴨 #癒し #duck #duckling #cute #nature #foryoupage",
        "title": "子鴨の行進がかわいすぎる🐥🐥🐥",
    },
    {
        "prompt": "tiny sugar glider gliding between trees at dusk, large eyes glowing, motion blur wings, forest canopy, photorealistic, magical atmosphere",
        "negative": "ugly, deformed, low quality",
        "caption": "夕暮れに滑空するフクロモモンガ🌅",
        "hashtags": "#フクロモモンガ #滑空 #動物 #sugarglider #gliding #cute #wildlife #viral",
        "title": "フクロモモンガの滑空が神秘的すぎる✨",
    },
]


def get_random_theme():
    return random.choice(THEMES)


def get_daily_themes(count=3):
    return random.sample(THEMES, min(count, len(THEMES)))
