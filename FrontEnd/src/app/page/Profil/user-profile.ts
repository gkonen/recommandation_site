import {Component, computed, inject, OnInit, signal} from '@angular/core';
import {DefaultUser, UserModel} from '../../api/UserModel';
import {ActivatedRoute} from '@angular/router';
import {CondensedMovie} from '../../component/condensed-movie/condensed-movie';
import {UserService} from '../../api/service/user-service';
import {MovieData} from '../../api/UserDataModel';
import {DataUser} from '../../api/ResponseData';

type category = {id : number, name : string}

@Component({
  selector: 'app-user-profile',
  imports: [
    CondensedMovie
  ],
  templateUrl: './user-profile.html',
  styleUrl: './user-profile.scss',
})
export class UserProfile implements OnInit {

  private userService = inject(UserService);
  private router = inject(ActivatedRoute)

  readonly categories = [
    {id : 1, name : "Tags"},
    {id : 2, name : "Ratings"}
  ]

  readonly user = signal<UserModel>(DefaultUser());
  readonly selectedCategory = signal<category>(this.categories[0]);

  readonly tags = signal<MovieData[]>([]);
  readonly ratings = signal<MovieData[]>([]);
  readonly viewData = computed(() => {
    if (this.selectedCategory().name == "Tags") return this.tags();
    else if(this.selectedCategory().name == "Ratings") return this.ratings();
    else return [];
  })

  ngOnInit() {
    this.router.queryParams.subscribe(params => {
      this.user.set({
        id: params["id"],
        username: params["username"],
        logged: params["logged"]
      })
    })
    this.loadData();
  }

  loadData() {
    this.userService.get_user_data(this.user()).subscribe((response : DataUser ) => {
      this.tags.set(response.tags)
      this.ratings.set(response.ratings)
      console.log(response);
    })
  }

  onCategoryClick(id : number) {
    this.selectedCategory.set(this.categories.find(c => c.id == id) as category);
  }
}
