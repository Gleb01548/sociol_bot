sociol_bot


## Описание

Бот отвечает на вопросы по социологии России на основе [аналитических обзоров ВЦИОМ](https://wciom.ru/analytical-reviews)

## Как это работает
По запросу пользователя осуществляется поиск аналитических обзоров ВЦИОМ, в качестве метрики сходства берется наибольшее косинусное сходство между запросом пользователя и названием аналитического доклада, его кратким описанием, "коротко о главном", его обзором.

Полученное N кол-во докладов переранжируются с помощью реранк модели.

Доклад с наибольшим скором подается в MinMax с вопросом пользователя. Ответ модели отрпаляется пользователю
вместе с контекстом.

В качестве эмбеддинг модели используется BAAI/bge-me, реранкера BAAI/bge-reranker-v2-gemma.

Чтобы получать более актуальные ответы указываете дату в вопросе, например вместо, "что россияне думают о полиции", спросите, "что россияне думали о полиции в 2024 году".
ы