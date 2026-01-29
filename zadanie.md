## Lista zadań do wykonania

1. [Model] 
    - Zainstaluj model llm bielik na komputerze lokalnym
    - Wersja to Bielik v3.0 11B GGUF
    - Utwórz plik download_model.pl, który pobierze odpowiednią wersję modelu z repozytorium Hugging Face
    - Utwórz plik app.py, który będzie serwerem Flask, który będzie serwował stronę www oraz będzie komunikował się z modelem llm. Aplikacja powinna miec możliwość debugowania. Powinna też próbować uruchomić model na GPU, jeśli jest dostępny, a jeśli nie, to uruchomić go na CPU
    - Utwórz plik templates/index.html, który będzie stroną www, która będzie komunikowała się z modelem llm
    - Utwórz plik static/style.css, który będzie stylem strony www
    - Utwórz plik static/script.js, który będzie skryptem strony www
    - Utwórz plik requirements.txt, który będzie zawierał listę zależności
    - Utwórz plik README.md, który będzie zawierał instrukcję instalacji i uruchomienia

2. [Strona WWW] 
    - Zapewnij dostęp do lokalnego modelu llm bielik poprzez stronę www działającą na lokalnym komputerze
    - Zmodyfikuj stronę główną llma tak, aby jej styl był zgodny z CSS z pliku index.html, który masz w katalogu sources
    - Ustaw skalowanie okna na stronie, aby dopasowywało się do rozmiaru przeglądarki zaraz po otwarciu strony
    - Dodaj do strony głównej ikonę pogody w Katowicach, temperaturę oraz czas systemowy - tak jak w pliku index.html
    - Użyj czasu na stronie bez podawania sekund, odświeżanie czasu może odbywać się co 30 sekund
    - W górnej środkowej częśći strony dodaj informację o wersji llma, a styl tej informacji powinien być taki sam jak zegara
    - Obok dymku konwersacji dodaj godzinę i minutę każdego dymka. Jeżeli dymek jest po lewej, to godinę dodaj po prawej - i odwrotnie. Niech ta godzina będzie w tym samym stylu co godzina na górze strony. Znacznik czasu powinien być odsunięty od dymku aż do końca ramki i powinno się to aktualizować po przeskalowaniu ramki lub okna
    

3. [Dokumentacja] 
    - Utwórz plik results.md i zapisuj w nim wszystkie kroki twojego działania , abyś mógł je później łatwo powtórzyć
    - Utwórz plik manual.md i zapisz w nim instrukcję włączania, wyłączania silnika modelu oraz sposób dostępu do interfejsu użytkownika
    - Utwórz plik adminguide.md z informacjami o ścieżkach w jakich zainstalowane są elementy llm oraz strony lokalnej www oraz o możliwościach debugowania pracy aplikacji
    - Utwórz plik .gitignore, który będzie zawierał listę plików i katalogów, które mają być ignorowane przez system kontroli wersji - np duże pliki modeli
    - Utwórz plik .env, który będzie zawierał zmienne środowiskowe
    - Utwórz plik .env.example, który będzie zawierał przykładowe zmienne środowiskowe

4. [Informacje] 
    - Utwórz plik info.md z informacjami o wersji systemu, wersji modelu, wersji strony www, wersji interfejsu użytkownika, wersji silnika modelu, wersji silnika strony www.

5. W razie problemów przerwij pracę i zapytaj mnie o zdanie czy potwierdzenie