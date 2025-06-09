import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LayoutComponent } from './components/layout/layout.component';
import { LoginComponent } from './components/login/login.component';

export const routes: Routes = [
    { path: '', component: LayoutComponent, children: [
        { path: 'dashboard', component: DashboardComponent },
    ]},
    { path: "login", component: LoginComponent}

];
