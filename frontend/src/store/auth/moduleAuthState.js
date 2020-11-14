export default {
  isUserLoggedIn: () => {
    return localStorage.getItem('userInfo')
  }
}
