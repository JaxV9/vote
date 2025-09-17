import { Injectable } from '@angular/core';
import { QuickHttp } from '@jaslay/http';

@Injectable()
export class HttpService {
  private baseUrl = 'http://localhost:7071/';
  private headers = {
    'Content-Type': 'application/json',
  };
  quickHttp = new QuickHttp(this.baseUrl, this.headers, 'omit');
  constructor() {}
}
