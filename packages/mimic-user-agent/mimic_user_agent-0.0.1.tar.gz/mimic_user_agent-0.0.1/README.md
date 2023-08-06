# random_user_agent

Funcion que retorna un 'user-agent' falso aleatorio o estático.

# Uso

```python
>>> from randomUserAgent import random_user_agent
>>> random_user_agent()
'Mozilla/5.0 (Windows NT 6.3; x86; rv:105.0) Gecko/20100101 Firefox/105.0'
>>>
>>> random_user_agent(1)
'Mozilla/5.0 (Windows NT 10.0; x86; rv:107.0) Gecko/20100101 Firefox/107.0'
```

Recibe un parámetro `int` para el uso de una *seed*, por defecto es `None`.

---

**Aclaración:**

Por ahora, solamente muestra usuarios Mozilla.

---

# Tests

```python
python -m unittest
```
