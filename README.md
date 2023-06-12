<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Mike7154/plex_criticker">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Plex Criticker</h3>

  <p align="center">
    Allows import of criticker ratings into plex
    <br />
    <a href="https://github.com/Mike7154/plex_criticker"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Mike7154/plex_criticker">View Demo</a>
    ·
    <a href="https://github.com/Mike7154/plex_criticker/issues">Report Bug</a>
    ·
    <a href="https://github.com/Mike7154/plex_criticker/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a tool that imports criticker ratings into plex. It can also create playlists for movies based on the ratings and PSI of the movie.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Python

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

* Python
* A plex account with a server
* A criticker account

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Mike7154/plex_criticker.git
   ```
2. Install requirements
   ```sh
   py -m pip install -r requirements.txt
   ```
3. Copy settings_template.yml to settings.yml
4. Edit settings.yml with your plex and criticker credentials

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To run the script, simply run the following command:
```sh
py import_criticker.py -arguments
```

### Arguments
print("Arguments include -f for file-read, -x for xml read, -i for import ratings, -c for collection build, -p for creating a collection sorted by PSI")
-f : Reads a file of movies and ratings. You can download a csv file from your criticker profile
-x : Reads an xml file of movies and ratings. You can get an xml url of recent ratings from your criticker profile. The URL must be pasted into the settings.yml file
-i : Imports ratings into plex
-c : Creates a collection of movies in plex based on the ratings. The name of this collection is set in the settings.yml file
-p : Creates a collection of movies in plex based on the PSI of the movie. The name of this collection is set in the settings.yml file



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/Mike7154/plex_criticker/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - Dr215.code@gmail.com.com

Project Link: [https://github.com/Mike7154/plex_criticker](https://github.com/Mike7154/plex_criticker)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Mike7154/plex_criticker.svg?style=for-the-badge
[contributors-url]: https://github.com/Mike7154/plex_criticker/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Mike7154/plex_criticker.svg?style=for-the-badge
[forks-url]: https://github.com/Mike7154/plex_criticker/network/members
[stars-shield]: https://img.shields.io/github/stars/Mike7154/plex_criticker.svg?style=for-the-badge
[stars-url]: https://github.com/Mike7154/plex_criticker/stargazers
[issues-shield]: https://img.shields.io/github/issues/Mike7154/plex_criticker.svg?style=for-the-badge
[issues-url]: https://github.com/Mike7154/plex_criticker/issues
[license-shield]: https://img.shields.io/github/license/Mike7154/plex_criticker.svg?style=for-the-badge
[license-url]: https://github.com/Mike7154/plex_criticker/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 