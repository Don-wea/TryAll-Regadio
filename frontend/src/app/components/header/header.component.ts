
import { Component, EventEmitter, Output } from '@angular/core';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-header',
  imports: [MatChipsModule, MatIconModule, MatButtonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  @Output() toggleSidenavEvent = new EventEmitter<void>();
  
  username = "Usuario";
  
  toggleSidenav() {
    this.toggleSidenavEvent.emit();
  }
}