def reserver_cours(request, cours_id):
    if not request.user.is_authenticated:
        return redirect('membres:inscription')
    
    cours = Cours.objects.get(id=cours_id)
    # Logique de réservation à implémenter
    # Créer une instance de Reservation
    return render(request, 'cours/confirmation_reservation.html', {'cours': cours})