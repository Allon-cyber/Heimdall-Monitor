#!/bin/bash

# Przejdź do katalogu, w którym znajduje się skrypt
cd "$(dirname "$0")"

echo "Dodawanie wszystkich zmian do poczekalni..."
git add .

# Sprawdź, czy są jakieś zmiany do zatwierdzenia
if git diff --cached --quiet; then
    echo "Brak zmian do zatwierdzenia."
else
    read -p "Podaj wiadomość do commita (domyślnie: 'Automatyczna aktualizacja'): " COMMIT_MESSAGE
    COMMIT_MESSAGE="${COMMIT_MESSAGE:-Automatyczna aktualizacja}"
    
    echo "Zatwierdzanie zmian z wiadomością: \"$COMMIT_MESSAGE\""
    git commit -m "$COMMIT_MESSAGE"
    
    echo "Pobieranie najnowszych zmian z GitHub przed wypychaniem..."
    git pull --rebase origin main
    
    echo "Wypychanie zmian do GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "Zmiany pomyślnie wypchnięte na GitHub!"
    else
        echo "Wystąpił błąd podczas wypychania zmian. Upewnij się, że masz skonfigurowany Personal Access Token (PAT) dla uwierzytelnienia."
    fi
fi
