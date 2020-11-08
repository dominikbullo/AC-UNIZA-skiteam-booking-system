# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [0.1.0](https://github.com/dominikbullo/sport_club_management_system/compare/v1.0.1-alpha.1...v0.1.0) (2020-11-08)


### ⚠ BREAKING CHANGES

* **accommodation:** Accommodation for events now could be added, updated and deleted by `any user` from application
* **deploy:** Pulling image from registry when deploying via CI
* **events:** new `/api/event-types` and `/api/event-types` endpoints and old are not fully compatible anymore

added need_ski parameter into location

Signed-off-by: Dominik Bullo <dominobullo@gmail.com>

Took 6 hours 42 minutes

### Features

* **accommodation:** Accommodation for events now could be added, updated and deleted by `any user` from application ([2abd263](https://github.com/dominikbullo/sport_club_management_system/commit/2abd2633604bde8d13c0256fa3137921d5337c35))
* **accommodation:** basic accommodation created on frontend ([d5a7141](https://github.com/dominikbullo/sport_club_management_system/commit/d5a7141850c7a5c6e4675f6937236ff29e00bed9)), closes [#sportagenda-32](https://github.com/dominikbullo/sport_club_management_system/issues/sportagenda-32)
* **events:** Fixed Edit Event component to be compatible with new api. Fixed creating new event in calendar. ([78e6995](https://github.com/dominikbullo/sport_club_management_system/commit/78e6995386ee172d98c7cfd73266e388b33d89ca))


### Bug Fixes

* calendar not selectable by coach ([a2a7801](https://github.com/dominikbullo/sport_club_management_system/commit/a2a78013bbf9cd2083c204f2fd8decd8c1c9bb1c))
* calendar not selectable by coach ([6370f9d](https://github.com/dominikbullo/sport_club_management_system/commit/6370f9d4ba6f01d010464da3c56166f9c8253581))
* calendar not selectable by coach ([6b6d2bc](https://github.com/dominikbullo/sport_club_management_system/commit/6b6d2bc2eb30eaefcd5a528ef5bca845738dbfbb))
* calendar not selectable by coach ([580a9c8](https://github.com/dominikbullo/sport_club_management_system/commit/580a9c84f5c389510b8c7d1e9f4c085a156558f0))
* Default season fixed ([d5078e5](https://github.com/dominikbullo/sport_club_management_system/commit/d5078e5e921142dcd5a38099b81c15b935972e32))
* **events:** Fixed edit event participants by adding new component [Dual Listbox](https://vuejsexamples.com/vue-multi-select-dual-listbox/) ([02c01fd](https://github.com/dominikbullo/sport_club_management_system/commit/02c01fdb94b0ff7487bc40b41837a0420f4723cf))


### ci

* **deploy:** Pulling image from registry when deploying via CI ([7a9e702](https://github.com/dominikbullo/sport_club_management_system/commit/7a9e702f132fadbd8e6452419bc80fa717fdd15f))
