 <div class="turtle-top-container">
        <!-- Left Section with Name -->
          
        </div>
        <div class="turtle-info">
            <h1>{{ turtle.name }}</h1>
            <table>
                <tr>
                    <th>Active</th>
                    <td>{{ 'Yes' if turtle.is_active else 'No' }}</td>
                </tr>
                <tr>
                    <th>Sex</th>
                    <td>{{ turtle.turtle_sex }}</td>
                </tr>
                <tr>
                    <th>Age</th>
                    <td>{{ turtle.turtle_age }}</td>
                </tr>
                <tr>
                    <th>Length</th>
                    <td>{{ turtle.length }} cm</td>
                </tr>
                <tr>
                    <th>Length Type</th>
                    <td>{{ turtle.length_type }}</td>
                </tr>
                <tr>
                    <th>Width</th>
                    <td>{{ turtle.width }} cm</td>
                </tr>
                <tr>
                    <th>Width Type</th>
                    <td>{{ turtle.width_type }}</td>
                </tr>
                <tr>
                    <th>Project Name</th>
                    <td>{{ turtle.project_name }}</td>
                </tr>

            </table>
        </div>

        <!-- Right Section with Picture -->

    </div>

    
    <div class="turtle-bottom-container">
   

  
    </div>