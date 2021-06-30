#include "color.h"
#include "ui_color.h"

color::color(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::color)
{
    ui->setupUi(this);
}

color::~color()
{
    delete ui;
}
