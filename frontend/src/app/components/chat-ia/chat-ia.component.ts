import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-chat-ia',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './chat-ia.component.html',
  styleUrls: ['./chat-ia.component.scss'],
})
export class ChatIaComponent {
  input = '';
  messages: { from: 'user' | 'ia', text: string }[] = [];
  loading = false;

  constructor(private http: HttpClient) {}

  sendMessage() {
    const userMsg = this.input.trim();
    if (!userMsg) return;

    this.messages.push({ from: 'user', text: userMsg });
    this.input = '';
    this.loading = true;

    this.http.post<any>('http://localhost:8000/api/chat/', { message: userMsg })
      .subscribe({
        next: (resp) => {
          this.messages.push({ from: 'ia', text: resp.response });
          this.loading = false;
        },
        error: (err) => {
          this.messages.push({ from: 'ia', text: 'Error al conectar con la IA.' });
          this.loading = false;
        }
      });
  }
}
