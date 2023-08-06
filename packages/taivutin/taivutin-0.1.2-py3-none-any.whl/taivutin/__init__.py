"""

Tässä on pelkistetty käyttöesimerkki alkuun pääsemiseksi

```python
from taivutin import Taivutin
t = Taivutin()
print(t.taivuta("makaronilaatikko", "talojen")) # 'makaronilaatikkojen'
print(t.taivuta("makaronilaatikko", "mon gen")) # 'makaronilaatikkojen'
```

Tarkempaa tietoa kannattaa etsiä [taivuttimen](taivutin/taivutin.html) ja [arvaimen](taivutin/arvain.html) dokumentaatiosivulta.

"""

from .taivutin import Taivutin
from .arvain import Arvain
