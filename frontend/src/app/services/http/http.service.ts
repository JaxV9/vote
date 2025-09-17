import { Injectable } from '@angular/core';
import { QuickHttp } from '@jaslay/http';

@Injectable()
export class HttpService {
  private baseUrl = 'https://votefunctions.azurewebsites.net/';
  private headers = {
    'Content-Type': 'application/json',
  };
  quickHttp = new QuickHttp(this.baseUrl, this.headers, 'omit');
  constructor() {}
}
