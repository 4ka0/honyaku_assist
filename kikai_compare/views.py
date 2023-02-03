from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


from .forms import InputForm


def input_page_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            # Process form data in form.cleaned_data as required
            return HttpResponseRedirect(reverse_lazy('output_page'))
    else:
        form = InputForm()
    return render(request, 'input.html', {'form': form})


def output_page_view(request):
    return render(request, 'output.html')
