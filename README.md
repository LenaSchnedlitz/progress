<p align="center">
  <img src="https://github.com/Mailea/progress/blob/master/progressbar/static/img/logo.png"/>
</p>


# Progress
Progress bars for your README files.   

## Themes 
#### Default
Used when no other theme is specified:  
<img src="https://progressbadges.herokuapp.com/79" width="100%">

#### Minimal
Produces simple progress bars without text:  
<img src="https://progressbadges.herokuapp.com/66/100/minimal" width="100%">

#### Badge
Makes progress bars look similar to the famous badges by [shields.io](https://shields.io):  
![Progress Badge](https://progressbadges.herokuapp.com/45/100/badge)

#### Custom Color
Looks like the default theme, but allows to set a custom color (in hex format, e.g. `00b1e9`):  
<img src="https://progressbadges.herokuapp.com/11/100/00b1e9" width="100%">


## How to Use
### Requirements
This program is written in **Python 3.6**.  
Requirements are listed in *requirements.txt* and can be installed with Pip:
```bash
cd progressbar
pip install -r requirements.txt
```

### Web App
The web app can be started by executing `app.py` inside the *progressbar* folder:
```python  
python app.py
```

#### URL Parameter
Progress bars can be requested directly using URL parameters, e.g. `localhost:5000/10`. URLs are structured as follows:
```
<base-URL>/<dividend>/<divisor[optional]>/<theme[optional]>
```

#### User Interface
Progress bars can also be created via UI. Simply fill out the form and click 'Create'.


## Online
To see the web app in action, click [here](https://progressbadges.herokuapp.com).
