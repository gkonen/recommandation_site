export interface UserModel {
  id: number;
  username: string;
  logged: boolean;
}

export function DefaultUser(): UserModel {
  return {
    id: -1,
    username: "",
    logged: false
  }
}
