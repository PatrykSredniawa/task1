# Model wybranej domeny to Przelewy Bankowe

## Opis zadania
---
Zaprojektowanie fragmentu aplikacji bankowej opierając się o zasadę Domain Driven Design. Zdecydowano się na wykonanie zadania w kontekście **Przelewów Bankowych**. Przelewy te będą obejmować tworzenie i realizację przelewów między kontami klientów. W modelu zawarto informację o encje, agregaty czy też obiekty wartości związane z tym procesem.

---

## Bounded Contexts, czyli definicja Ograniczonego Kontekstu
---
Bounded Contexts definiuje granice i kontekst, w którym używane są podane niżej terminy.
- **Kontekst zarządzania Kontem** - utrzymywanie danych o kontach, numerach kont, salda.
- **Kontekst przelewów** - tworzenie i realizacja przelewów między kontami.
- **Kontekst uwierzytelnienia** - logowanie użytkowników wraz z autoryzacją operacji bankowych, w tym przypadku przelewów.

---

## Model
---
Poniższy schemat przedstawia trzy główne Agregaty (Roots):
- KontoBankowe
- Klient
- Przelew

![Model](DDDModel.png)


## Encje, Agregaty i Obiekty Wartości
---
| Typ                 | Nazwa          | Atrybuty                                                                                                                                                                                           | Rola                                                                    |
| ------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Agregat**         | KontoBankowe   | NumerKonta (Encja ID), saldo (Obiekt Wartości), waluta (Obiekt Wartości), <br>idKlienta (Referencja do idKlienta).                                                                                 | Reprezentuje konto klienta, przechowauje saldo oraz id właściciela.     |
| Agregat             | Klient         | idKlienta (Encja ID), DaneOsobowe (Obiekt Wartości).                                                                                                                                               | Zapewnia integralność danych osobowych klienta.                         |
| Agregat            | Przelew        | idTransakcji (Encja ID), KwotaPrzelewu (Obiekt Wartości), Waluta (Obiekt Wartości), NumerKontaNadawcy (Referencja do idKlienta Nadawcy),<br>NumerKontaOdbiorcy (Referencja do idKlienta Odbiorcy). | Reprezentuje proces przekazania środków między dwoma kontami bankowymi. |
| **Encja**           | NumerKonta     | numerIBAN: string                                                                                                                                                                                  | Identyfikuje konto w systemie; unikalne w całym systemie bankowym       |
| Encja               | idKlienta      | id: string(UUID)                                                                                                                                                                                   | Unikalny identyfikator klienta wewnątrz banku.                          |
| Encja               | idTransakcji   | id: string(UUID)                                                                                                                                                                                   | Unikalny identyfikator przelewu.                                        |
| **Obiekt Wartości** | Saldo          | kwota: decimal                                                                                                                                                                                     | Określa aktualną wartość środków dostępnych na koncie.                  |
| **Obiekt Wartości** | Waluta         | kod_waluty: string                                                                                                                                                                                | Umożliwia rozróżnianie walut w systemie bankowym (np. PLN, EUR).        |
| **Obiekt Wartości** | DaneOsobowe    | Imie: string, Nazwisko: string, Adres: string, pesel: string, numerTelefonu: string                                                                                                                | Dane pozwalające zidentyfikować daną osobę oraz mieć kontakt z nią.     |
| **Obiekt Wartości** | Kwota Przelewu | wartość: decimal, waluta: string                                                                                                                                                                   | Określa kwotę i walutę przelewu. Niezmienny obiekt wartości.            |
---


## Założenia, ograniczenia 
---
### Założenia ogólne
 1. System bankowy został podzielony na trzy niezależne **bounded contexty**:
   - **Zarządzanie kontem** (KontoBankowe),
   - **Zarządzanie klientem** (Klient),
   - **Obsługa przelewów** (Przelew).
2. Wszystkie identyfikatory (`idKlienta`, `idTransakcji`, `NumerKonta`) są unikalne i generowane centralnie w ramach odpowiedniego kontekstu.
3. System obsługuje wyłącznie waluty zdefiniowane w tabeli `Waluta` (np. PLN, EUR, USD).

### Ograniczenia 
| Obszar | Ograniczenie |
|--------|---------------|
| **KontoBankowe** | Saldo nie może być ujemne (brak debetu w tym modelu). |
| **KontoBankowe** | Każde konto jest przypisane dokładnie do jednego klienta. |
| **Przelew** | Kwota przelewu musi być większa od zera. |
| **Przelew** | Przelew może być wykonany tylko między kontami w tej samej walucie. |
| **Przelew** | Nie można wykonać przelewu na to samo konto. |
| **Klient** | PESEL musi być unikalny w systemie. |
| **Klient** | Dane osobowe są niezmienne po utworzeniu obiektu Klient (zmiana = utworzenie nowej wersji). |

---

### Operacje
| Agregat | Operacja | Opis |
|----------|-----------|------|
| **KontoBankowe** | `zasil(kwota)` | Dodaje środki do salda konta. |
| **KontoBankowe** | `obciąż(kwota)` | Odejmuje środki z salda, jeśli saldo jest wystarczające. |
| **Przelew** | `wykonaj()` | Realizuje przelew między kontami. Tworzy zdarzenie `PrzelewZrealizowany`. |

