var GaussianNB = function(priors, sigmas, thetas) {

    this.priors = priors;
    this.sigmas = sigmas;
    this.thetas = thetas;

    this.predict = function(features) {
        var likelihoods = new Array(this.sigmas.length);
    
        for (var i = 0, il = this.sigmas.length; i < il; i++) {
            var sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.log(2. * Math.PI * this.sigmas[i][j]);
            }
            var nij = -0.5 * sum;
            sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.pow(features[j] - this.thetas[i][j], 2.) / this.sigmas[i][j];
            }
            nij -= 0.5 * sum;
            likelihoods[i] = Math.log(this.priors[i]) + nij;
        }
    
        var classIdx = 0;
        for (var i = 0, l = likelihoods.length; i < l; i++) {
            classIdx = likelihoods[i] > likelihoods[classIdx] ? i : classIdx;
        }
        return classIdx;
    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 8) {

        // Features:
        var features = process.argv.slice(2);

        // Parameters:
        var priors = [0.5735977695627144, 0.4264022304372856];
        var sigmas = [[0.36499890555977155, 0.36623189761802055, 1.0000000000105063e-09, 2.485227876048033e-05, 1.7416244234876965, 0.10266989149642149, 1.4778645899937055, 0.9262718998608906], [1.125696019214256, 1.4002993684534342, 2.344419877600619, 2.3451550186406114, 0.00023466225771714074, 1.7447278179694106, 0.3521462736268731, 1.0923196410404898]];
        var thetas = [[-0.48054426891444524, -0.378620324652921, -0.015760403522919877, -0.0021837773490583057, 0.0259813829882183, -0.38283148118220084, 0.03992453464215766, -0.04663017101869356], [0.6464298288085631, 0.5093213830269545, 0.02120094986096054, 0.002937624916635942, -0.034950247133761735, 0.5149862454964695, -0.05370662343402985, 0.06272706890697753]];

        // Estimator:
        var clf = new GaussianNB(priors, sigmas, thetas);
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}