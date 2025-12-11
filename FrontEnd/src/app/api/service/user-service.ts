import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {UserModel} from '../UserModel';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private url = 'http://localhost:5000/';
  private http = inject(HttpClient);

  connect(user:string, password:string) : UserModel {
    return {
      logged: true,
      username: "User",
      id: 42,
    }
  }

}
