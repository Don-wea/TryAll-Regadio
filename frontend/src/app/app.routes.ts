import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LayoutComponent } from './components/layout/layout.component';

export const routes: Routes = [
    { path: '', component: LayoutComponent, children: [
        { path: 'dashboard', component: DashboardComponent },
    ]}
];
