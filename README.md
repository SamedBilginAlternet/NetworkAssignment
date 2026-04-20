# Network Assignment — Edge Integrity & Edge Rupture Degree

Ayrıt Bütünlük ve Ayrıt Parçalanma Derecesi hesaplama — Kaba Kuvvet Yöntemi

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `graph_analysis.py` | Brute force algoritması (Edge Integrity + Edge Rupture Degree) |
| `rapor.pdf` | Ödev raporu |
| `requirements.txt` | Python bağımlılıkları |

## Çalıştırma

```bash
pip install -r requirements.txt
python graph_analysis.py
```

## Tanımlar

**Edge Integrity:**
```
I'(G) = min_{F ⊆ E(G)} { |F| + m(G−F) }
```

**Edge Rupture Degree:**
```
r'(G) = max_{F ⊆ E(G), ω(G−F)>1} { ω(G−F) − |F| − m(G−F) }
```

## Sonuçlar

| Graf | n | e | I'(G) | r'(G) |
|------|---|---|-------|-------|
| P_10 | 10 | 9  | 6  | 0   |
| C_10 | 10 | 10 | 7  | -1  |
| S_10 | 10 | 9  | 10 | -9  |
| W_10 | 10 | 18 | 6  | -5  |
| K_10 | 10 | 45 | 10 | -16 |
