import React, { createContext } from "react";
import { UserData } from "../utils/backend";

const UserContext = createContext<UserData>({
  name: '',
  surname: '',
  patronymic: '',
  phone_number: '',
  email: '',
  birthday: '',
  position: '',
  isDoctor: false,
  avatar: 'user.svg',
  _id: '',
  city: ""
});

export default UserContext;