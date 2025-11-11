import plotext as plt  # To jest biblioteka do wykresów
from rich.console import Console
from rich.panel import Panel

console = Console()

# 1. Przygotuj dane do wykresu (np. funkcja sinus)
y_dane = plt.sin() 

# 2. Użyj plotext do "narysowania" wykresu
plt.plot(y_dane)
plt.title("Wykres Liniowy (Sinusoida)")
plt.plotsize(70, 20) # Ustawiamy rozmiar w znakach

# 3. Zamiast pokazywać (plt.show()), "budujemy" wykres do stringa
wykres_jako_tekst = plt.build()

# 4. Czyścimy ustawienia plotext po użyciu
plt.clf() 

# 5. A teraz "mega" część:
# Drukujemy ten wykres-tekstowy za pomocą Panelu rich
console.print(
    Panel(
        wykres_jako_tekst,
        title="[bold green]Wykres z 'plotext' w Panelu 'rich'[/]",
        border_style="blue",
        padding=1
    )
)