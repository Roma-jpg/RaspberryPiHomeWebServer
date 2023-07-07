import subprocess
from django.shortcuts import render, redirect
from .models import Command

def terminal_page(request):
    commands = Command.objects.order_by('-created_at')
    return render(request, 'terminal.html', {'commands': commands})

def execute_command(request):
    if request.method == 'POST':
        command_text = request.POST.get('command')
        output_text = execute_terminal_command(command_text)
        command = Command.objects.create(command_text=command_text, output_text=output_text)
        return redirect('terminal_page')

def execute_terminal_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        output = error
    return output.decode(encoding="cp1251")
