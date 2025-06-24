import matplotlib.pyplot as plt
from io import BytesIO
import base64

def get_chart(chart_type, df):
    plt.switch_backend('AGG')  # Use non-GUI backend for server
    
    fig = plt.figure(figsize=(8, 4))
    fig.clf()  # Clear figure

    titles = df['title']
    cooking_times = df['cooking_time']

    if chart_type == 'bar':
        plt.bar(titles, cooking_times, color='orange')
        plt.xlabel('Recipe Title')
        plt.ylabel('Cooking Time (mins)')
        plt.title('Cooking Time per Recipe')
        plt.xticks(rotation=45, ha='right')

    elif chart_type == 'pie':
        plt.pie(cooking_times, labels=titles, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title('Cooking Time Distribution')

    elif chart_type == 'line':
        plt.plot(titles, cooking_times, marker='o', color='orange')
        plt.xlabel('Recipe Title')
        plt.ylabel('Cooking Time (mins)')
        plt.title('Cooking Time Trend')
        plt.xticks(rotation=45, ha='right')

    else:
        plt.text(0.5, 0.5, 'Invalid chart type selected', ha='center', va='center', fontsize=12)

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close(fig)  # Close the figure to free memory
    return image_base64