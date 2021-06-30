#ifndef COLOR_H
#define COLOR_H

#include <QWidget>

namespace Ui {
class color;
}

class color : public QWidget
{
    Q_OBJECT

public:
    explicit color(QWidget *parent = nullptr);
    ~color();

private:
    Ui::color *ui;
};

#endif // COLOR_H
