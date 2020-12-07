# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [0.3.1](https://github.com/dominikbullo/SportAgenda/compare/v0.3.0...v0.3.1) (2020-12-07)


### ⚠ BREAKING CHANGES

* **family:** Merging family from one to another family with all members by token

### Features

* **child_form:** Add child form active color on fields and added backend errors ([3cbe45f](https://github.com/dominikbullo/SportAgenda/commit/3cbe45fc078a2e5b3902e4d1fd1e6d2ee12d1665))
* **children:** Sending verification email if they have one ([9836e81](https://github.com/dominikbullo/SportAgenda/commit/9836e81b01e58b97f52c820601151503bf050c24)), closes [SA-59](https://sportagenda.myjetbrains.com/youtrack/issue/SA-59)
* **family:** Merging family from one to another family with all members by token ([7c3e167](https://github.com/dominikbullo/SportAgenda/commit/7c3e167cb3c38d50ce10d3a3e43707277c146387)), closes [SA-57](https://sportagenda.myjetbrains.com/youtrack/issue/SA-57)
* **registration:** Added email templates, handler success/failed verify email and redirect after registration. ([82de272](https://github.com/dominikbullo/SportAgenda/commit/82de2723c54eab139307f771ec65054ed611cd02))


### Bug Fixes

* User changed to another user (wrong store call from family change) ([66e6d2e](https://github.com/dominikbullo/SportAgenda/commit/66e6d2eb54a96c9831bede9cd0782063f0a3be58))

## [0.3.0](https://github.com/dominikbullo/sport_club_management_system/compare/v0.2.0...v0.3.0) (2020-12-03)


### ⚠ BREAKING CHANGES

* **calendar:** Events now can handle all day events, even with datepicker in popups.
* **database:** Database now could be on port from .env file

### Features

* **calendar:** Events now can handle all day events, even with datepicker in popups. ([86fbf29](https://github.com/dominikbullo/sport_club_management_system/commit/86fbf29d48d571d5c02d44cf70e441c840dfd25f)), closes [SA-33](https://sportagenda.myjetbrains.com/youtrack/issue/SA-33)


### Bug Fixes

* **child:** Adding child should now work without problems ([801bddb](https://github.com/dominikbullo/sport_club_management_system/commit/801bddb5c7020c3f53688fbc5d33b480111a3318))
* **database:** Database now could be on port from .env file ([f4f4e5d](https://github.com/dominikbullo/sport_club_management_system/commit/f4f4e5d94f40f1441b824db0f629b75eed23e325)), closes [SA-24](https://sportagenda.myjetbrains.com/youtrack/issue/SA-24) [SA-7](https://sportagenda.myjetbrains.com/youtrack/issue/SA-7)
* **statistics:** Fixed stats working with new APIs ([4b3f637](https://github.com/dominikbullo/sport_club_management_system/commit/4b3f63728d88917226801e97c3064ae2b9aa411d)), closes [SA-31](https://sportagenda.myjetbrains.com/youtrack/issue/SA-31) [SA-28](https://sportagenda.myjetbrains.com/youtrack/issue/SA-28)

## [0.2.0](https://github.com/dominikbullo/sport_club_management_system/compare/v0.1.0...v0.2.0) (2020-11-14)


### ⚠ BREAKING CHANGES

* **event_detail:** `event/change` has changed to accept array `"participants":[]` and filter only request user children
* remove unused boiler template
* **child:** Child username generate automatically (firs+last name + number) #sportagenda-45 fixed
* **authentication:** Users can now reset their forgotten password via email #sportagenda-43 fixed
* Using [Multiple Compose files](https://docs.docker.com/compose/extends/) to share components and extending services

### Features

* **authentication:** Users can now reset their forgotten password via email #[sportagenda-43](https://sportagenda.myjetbrains.com/youtrack/issue/sportagenda-43) fixed ([c8062c2](https://github.com/dominikbullo/sport_club_management_system/commit/c8062c2f4ae8629fc621417244668851ec4bd7a6))
* **child:** Child username generate automatically (firs+last name + number) #[sportagenda-45](https://sportagenda.myjetbrains.com/youtrack/issue/sportagenda-45) fixed ([1b7aa6c](https://github.com/dominikbullo/sport_club_management_system/commit/1b7aa6ce670b511f2809e69a918b6ffacafc7e52))
* **database:** Added database backups to production docker-compose file ([281f850](https://github.com/dominikbullo/sport_club_management_system/commit/281f850da8b9036eb1771a008276a802cc72cfe1))
* Event tab showing in calendar promp ([79bcde6](https://github.com/dominikbullo/sport_club_management_system/commit/79bcde6614a09a928d2642579ba5257789efac27))


### Bug Fixes

* .env file on prod server was badly configured,that caused not sending emails from prod version ([14c58f6](https://github.com/dominikbullo/sport_club_management_system/commit/14c58f69ee11b68b482e55f8ddb82c20f54157e3)), closes [sportagenda-21](https://sportagenda.myjetbrains.com/youtrack/issue/sportagenda-21)
* **event_edit:** Fixed event edit by filtering IDs from items, but it will need to be reopen according to [sportagenda-34](https://sportagenda.myjetbrains.com/youtrack/issue/sportagenda-34) ([d20048a](https://github.com/dominikbullo/sport_club_management_system/commit/d20048a468ee6b0d4c86853ca12f1448da74415d)), closes [sportagenda-32](https://sportagenda.myjetbrains.com/youtrack/issue/sportagenda-32)
* validation for sidebar ([b5cb43a](https://github.com/dominikbullo/sport_club_management_system/commit/b5cb43adbd915229b5992e3772837d4587542c29))


### ci

* Using [Multiple Compose files](https://docs.docker.com/compose/extends/) to share components and extending services ([23bf054](https://github.com/dominikbullo/sport_club_management_system/commit/23bf054a92d21236d44bbe0c6927ad88b42fc207))
* **event_detail:** Event detail prompt and tabs as separate components ([bbea561](https://github.com/dominikbullo/sport_club_management_system/commit/bbea5615eb8e591548e0f7425f319807a6563dfa))
* remove unused boiler template ([787bc34](https://github.com/dominikbullo/sport_club_management_system/commit/787bc34200b01c2c4cad4e546848be4a8169f4d8))

## [0.1.0](https://github.com/dominikbullo/sport_club_management_system/compare/v1.0.1-alpha.1...v0.1.0) (2020-11-08)


### ⚠ BREAKING CHANGES

* **accommodation:** Accommodation for events now could be added, updated and deleted by `any user` from application
* **deploy:** Pulling image from registry when deploying via CI
* **events:** new `/api/event-types` and `/api/event-types` endpoints and old are not fully compatible anymore

### Features

* **accommodation:** Accommodation for events now could be added, updated and deleted by `any user` from application ([2abd263](https://github.com/dominikbullo/sport_club_management_system/commit/2abd2633604bde8d13c0256fa3137921d5337c35))
* **accommodation:** basic accommodation created on frontend ([d5a7141](https://github.com/dominikbullo/sport_club_management_system/commit/d5a7141850c7a5c6e4675f6937236ff29e00bed9)), closes [#sportagenda-32](https://github.com/dominikbullo/sport_club_management_system/issues/sportagenda-32)
* **events:** Fixed Edit Event component to be compatible with new api. Fixed creating new event in calendar. ([78e6995](https://github.com/dominikbullo/sport_club_management_system/commit/78e6995386ee172d98c7cfd73266e388b33d89ca))


### Bug Fixes

* calendar not selectable by coach ([a2a7801](https://github.com/dominikbullo/sport_club_management_system/commit/a2a78013bbf9cd2083c204f2fd8decd8c1c9bb1c))
* Default season fixed ([d5078e5](https://github.com/dominikbullo/sport_club_management_system/commit/d5078e5e921142dcd5a38099b81c15b935972e32))
* **events:** Fixed edit event participants by adding new component [Dual Listbox](https://vuejsexamples.com/vue-multi-select-dual-listbox/) ([02c01fd](https://github.com/dominikbullo/sport_club_management_system/commit/02c01fdb94b0ff7487bc40b41837a0420f4723cf))


### ci

* **deploy:** Pulling image from registry when deploying via CI ([7a9e702](https://github.com/dominikbullo/sport_club_management_system/commit/7a9e702f132fadbd8e6452419bc80fa717fdd15f))
