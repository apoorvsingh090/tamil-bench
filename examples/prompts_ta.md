# TPL-Bench — Tamil prompts (copy-paste)

Scored evaluation prompts/passages/answers are in Tamil. Do not translate to English at test time.
Exception: `nadai`-track items may contain documented Tanglish/English/Roman spans by design.
(Meta-docs — schema notes, judge settings, `explanation_ta` — may use English.)

## MCQ / short answer

```
அறிவுறுத்தல் — சரியான பதில் மட்டும் எழுதுக, விளக்கம் தர வேண்டாம்.
பத்தி: {passage_ta}
கேள்வி: {prompt_ta}
விருப்பங்கள்: {choices}
பதில்:
```

## இலக்கணத் திருத்தம்

```
அறிவுறுத்தல் — தவறான வாக்கியத்தை திருத்தி சரியான வாக்கியம் மட்டும் எழுதுக.
தவறு: {prompt_ta}
சரி:
```

## சுருக்கம்

```
அறிவுறுத்தல் — கீழே உள்ள பத்தியை சுருக்கி எழுதுக. பெயர், எண், உண்மை மாறக் கூடாது, புது செய்தி சேர்க்கக் கூடாது.
பத்தி: {passage_ta}
சுருக்கம்:
```

## எழுத்து

```
அறிவுறுத்தல்: {prompt_ta}
சொல் வரம்பை பின்பற்றுக. சரியான தெளிவான ஒழுங்கான தமிழில் எழுதுக.
```

## grounded QA (anti-hallucination, MCQ உட்பட)

```
அறிவுறுத்தல் — பதில் கொடுத்த பகுதிகளிலிருந்து மட்டும் தருக, மூலம் [பகுதி 1]/[பகுதி 2] காட்டி எழுதுக. பகுதிகளில் பதில் இல்லையெனில் எழுதுக: தகவல் இல்லை.
பகுதிகள்: {passage_ta}
கேள்வி: {prompt_ta}
விருப்பங்கள் (இருந்தால்): {choices}
பதில்:
```
