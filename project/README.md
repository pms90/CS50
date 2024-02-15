# Autodim
#### Video Demo:  https://youtu.be/i5mnWl2LIO0
#### Description:

The objective of this project is to automate the measurement of sides and interior angles of a polyline in autocad software.

The usual way of making these measurements and fixing the legends corresponding to each measurement is simply to do it by hand. This task becomes repetitive and tedious. Especially when polygons with a large number of sides have to be measured. Automating this measurement can reduce hours of human work to a simple click.

In addition to making measurements, this application allows you to interactively view the polygon with its linear and angular measurements thanks to the use of the Bokeh library. The fact of being able to zoom and move around the polygon allows the user to correctly visualize the measurement labels even when under normal conditions they would be superimposed.

The procedure to use this application is simple. The application is only 25.4 kb in size and can be quickly hosted on any server or delivered as a single html file. The logic of the application is written in python using the numpy library for the necessary calculations and Bokeh for the interactive graphs.

On the user side, the procedure to use the application consists of first running the "LIST" command of Autocad on the polyline to be sized. This command returns in text form all the coordinates of each one of the vertices of the polyline. The second and last step consists of copying the text with the coordinates and then pasting it into the <textarea> of the web application. Once the button "Medir" (Measure in Spanish) is clicked, all the measurements will be calculated and the interactive graph will be created to be able to visualize them.

Thanks to the use of the py-script framework, it was possible to implement this application in such a way that it can work entirely in the user's browser without having to depend on a server, or APIs, or usage fees.

Limitations: the measurement of polylines is limited to polylines at level 0, that is, the differences in the Z coordinates of the vertices will not be taken into account. Eventually the code of this project could be extended to cover those cases. Another limitation is that the polylines must be closed polylines

The main motivation for making this web application was the fact that polyline measurements in autocad were made daily by hand in my workplace. Measuring the sides and internal angles of a polyline or polygon with about 20 or 30 sides can take 10 or 15 minutes. In addition, formatting the measurement labels so that they are visible at a convenient scale is also time consuming. Time is not the only cost of performing this task, but it must also be considered that it is a visually tiring task. For this reason, I believe that this application has the potential to both reduce the human working time necessary to perform tasks that require these measurements and at the same time improve working conditions in terms of occupational health.

Thanks to py-script it was possible to become independent from the use of apis or user-server communication. You can even use the application without an internet connection assuming you have the application's atodim.html file on disk beforehand.

Pablo Manera

La Plata, Buenos Aires, Argentina  28/05/2023